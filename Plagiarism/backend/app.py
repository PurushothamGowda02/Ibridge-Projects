from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from database import get_connection, init_db
from plagiarism_engine import top_matches

app = Flask(__name__)
CORS(app)

# File upload configuration
UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    """Extract text from uploaded file based on extension"""
    ext = filepath.rsplit('.', 1)[1].lower()
    
    if ext == 'txt':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif ext == 'pdf':
        try:
            import PyPDF2
            text = ""
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    elif ext in ['doc', 'docx']:
        try:
            import docx
            doc = docx.Document(filepath)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    return ""


@app.route("/api/health", methods=["GET"])
def health():
    # Check if Google API is configured
    try:
        from config import is_google_api_configured
        google_api_configured = is_google_api_configured()
    except:
        google_api_configured = False
    
    return jsonify({
        "status": "ok",
        "service": "plagiarism-detector",
        "online_checking": {
            "available": True,
            "google_api_configured": google_api_configured,
            "method": "Google Custom Search API" if google_api_configured else "Fallback (may not work)"
        }
    })


@app.route("/api/documents", methods=["POST"])
def add_document():
    payload = request.get_json(force=True)
    title = (payload.get("title") or "").strip()
    author = (payload.get("author") or "").strip()
    raw_text = (payload.get("raw_text") or "").strip()

    if not title or not raw_text:
        return jsonify({"error": "title and raw_text are required"}), 400

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO documents (title, author, raw_text) VALUES (?, ?, ?)",
            (title, author, raw_text),
        )
        doc_id = cursor.lastrowid

    return jsonify({"message": "Document saved", "document_id": doc_id}), 201


@app.route("/api/documents", methods=["GET"])
def list_documents():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, author, LENGTH(raw_text) as text_length, created_at FROM documents ORDER BY id DESC"
        ).fetchall()
    
    documents = []
    for row in rows:
        doc_dict = dict(row)
        # Add a preview of the text
        full_text = conn.execute("SELECT raw_text FROM documents WHERE id = ?", (row['id'],)).fetchone()
        if full_text:
            preview = full_text['raw_text'][:200] + "..." if len(full_text['raw_text']) > 200 else full_text['raw_text']
            doc_dict['preview'] = preview
        documents.append(doc_dict)
    
    return jsonify(documents)


@app.route("/api/check", methods=["POST"])
def check_plagiarism():
    payload = request.get_json(force=True)
    title = (payload.get("title") or "Submitted Document").strip()
    text = (payload.get("raw_text") or "").strip()
    author = (payload.get("author") or "").strip()
    check_online = payload.get("check_online", False)  # New parameter
    
    print(f"DEBUG: check_online parameter = {check_online} (type: {type(check_online)})")

    if not text:
        return jsonify({"error": "raw_text is required"}), 400

    with get_connection() as conn:
        # Get corpus excluding documents with same title (case-insensitive)
        corpus_rows = conn.execute(
            "SELECT id, title, raw_text FROM documents WHERE LOWER(TRIM(title)) != LOWER(TRIM(?)) ORDER BY id ASC",
            (title,)
        ).fetchall()
        corpus = [(row["id"], row["title"], row["raw_text"]) for row in corpus_rows]

        matches = top_matches(text, corpus, limit=5) if corpus else []

        # Check online if requested
        online_matches = []
        if check_online:
            try:
                from web_search import check_online_plagiarism
                print("Checking online sources...")
                online_matches = check_online_plagiarism(text, num_searches=3)
                print(f"Found {len(online_matches)} online sources")
            except Exception as e:
                print(f"Online check error: {e}")

        # Check if document with same title already exists
        existing = conn.execute(
            "SELECT id FROM documents WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (title,)
        ).fetchone()

        if existing:
            # Update existing document instead of creating duplicate
            conn.execute(
                "UPDATE documents SET author = ?, raw_text = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?",
                (author, text, existing["id"])
            )
            source_id = existing["id"]
            
            # Delete old comparisons for this document
            conn.execute("DELETE FROM comparisons WHERE source_doc_id = ?", (source_id,))
        else:
            # Insert new document
            insert_cursor = conn.execute(
                "INSERT INTO documents (title, author, raw_text) VALUES (?, ?, ?)",
                (title, author, text),
            )
            source_id = insert_cursor.lastrowid

        # Insert new comparisons
        for match in matches:
            conn.execute(
                """
                INSERT INTO comparisons (source_doc_id, compared_doc_id, similarity_score, verdict)
                VALUES (?, ?, ?, ?)
                """,
                (source_id, match["doc_id"], match["final_score"], match["verdict"]),
            )

    # Combine database and online matches
    all_matches = matches + online_matches
    all_matches.sort(key=lambda x: x['final_score'], reverse=True)
    
    # Determine overall verdict
    if all_matches:
        highest_score = all_matches[0]['final_score']
        if highest_score >= 75:
            overall_verdict = "High plagiarism risk"
        elif highest_score >= 45:
            overall_verdict = "Moderate plagiarism risk"
        else:
            overall_verdict = "Low plagiarism risk"
    else:
        overall_verdict = "No corpus available"

    return jsonify(
        {
            "submitted_document_id": source_id,
            "matches": all_matches[:10],  # Top 10 total matches
            "database_matches": len(matches),
            "online_matches": len(online_matches),
            "overall_verdict": overall_verdict,
        }
    )


@app.route("/api/reports/<int:doc_id>", methods=["GET"])
def get_report(doc_id: int):
    with get_connection() as conn:
        doc = conn.execute(
            "SELECT id, title, author, created_at FROM documents WHERE id = ?", (doc_id,)
        ).fetchone()
        if not doc:
            return jsonify({"error": "Document not found"}), 404

        rows = conn.execute(
            """
            SELECT c.id, c.compared_doc_id, d.title AS compared_title, c.similarity_score, c.verdict, c.created_at
            FROM comparisons c
            JOIN documents d ON d.id = c.compared_doc_id
            WHERE c.source_doc_id = ?
            ORDER BY c.similarity_score DESC
            """,
            (doc_id,),
        ).fetchall()

    return jsonify(
        {
            "document": dict(doc),
            "comparisons": [dict(row) for row in rows],
        }
    )


@app.route("/api/check-file", methods=["POST"])
def check_file():
    """Handle file upload and plagiarism check"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use .txt, .pdf, .doc, or .docx"}), 400
    
    title = request.form.get('title', 'Uploaded Document').strip()
    author = request.form.get('author', '').strip()
    check_online = request.form.get('check_online', 'false').lower() == 'true'
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text
        text = extract_text_from_file(filepath)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if not text or len(text.strip()) < 10:
            return jsonify({"error": "Could not extract sufficient text from file"}), 400
        
        # Process plagiarism check (same as text endpoint)
        with get_connection() as conn:
            # Get corpus excluding documents with same title
            corpus_rows = conn.execute(
                "SELECT id, title, raw_text FROM documents WHERE LOWER(TRIM(title)) != LOWER(TRIM(?)) ORDER BY id ASC",
                (title,)
            ).fetchall()
            corpus = [(row["id"], row["title"], row["raw_text"]) for row in corpus_rows]

            matches = top_matches(text, corpus, limit=5) if corpus else []

            # Check online if requested
            online_matches = []
            if check_online:
                try:
                    from web_search import check_online_plagiarism
                    print("Checking online sources for uploaded file...")
                    online_matches = check_online_plagiarism(text, num_searches=2)
                    print(f"Found {len(online_matches)} online sources")
                except Exception as e:
                    print(f"Online check error: {e}")

            # Check if document with same title already exists
            existing = conn.execute(
                "SELECT id FROM documents WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
                (title,)
            ).fetchone()

            if existing:
                # Update existing document
                conn.execute(
                    "UPDATE documents SET author = ?, raw_text = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (author, text, existing["id"])
                )
                source_id = existing["id"]
                # Delete old comparisons
                conn.execute("DELETE FROM comparisons WHERE source_doc_id = ?", (source_id,))
            else:
                # Insert new document
                insert_cursor = conn.execute(
                    "INSERT INTO documents (title, author, raw_text) VALUES (?, ?, ?)",
                    (title, author, text),
                )
                source_id = insert_cursor.lastrowid

            # Insert new comparisons
            for match in matches:
                conn.execute(
                    """
                    INSERT INTO comparisons (source_doc_id, compared_doc_id, similarity_score, verdict)
                    VALUES (?, ?, ?, ?)
                    """,
                    (source_id, match["doc_id"], match["final_score"], match["verdict"]),
                )

        # Combine database and online matches
        all_matches = matches + online_matches
        all_matches.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Determine overall verdict
        if all_matches:
            highest_score = all_matches[0]['final_score']
            if highest_score >= 75:
                overall_verdict = "High plagiarism risk"
            elif highest_score >= 45:
                overall_verdict = "Moderate plagiarism risk"
            else:
                overall_verdict = "Low plagiarism risk"
        else:
            overall_verdict = "No corpus available"

        return jsonify(
            {
                "submitted_document_id": source_id,
                "matches": all_matches[:10],
                "database_matches": len(matches),
                "online_matches": len(online_matches),
                "overall_verdict": overall_verdict,
            }
        )
    
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500


@app.route("/api/cleanup-duplicates", methods=["POST"])
def cleanup_duplicates():
    """Remove duplicate documents from database"""
    try:
        from db_utils import remove_duplicate_documents, get_document_stats
        
        stats_before = get_document_stats()
        removed = remove_duplicate_documents()
        stats_after = get_document_stats()
        
        return jsonify({
            "success": True,
            "removed_count": removed,
            "before": stats_before,
            "after": stats_after
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

