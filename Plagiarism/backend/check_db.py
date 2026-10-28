"""Check what documents are in the database"""
from database import get_connection

with get_connection() as conn:
    docs = conn.execute('SELECT id, title, LENGTH(raw_text) as length FROM documents').fetchall()
    
    print(f"\n{'='*80}")
    print(f"DOCUMENTS IN DATABASE: {len(docs)}")
    print(f"{'='*80}\n")
    
    if docs:
        for doc in docs:
            print(f"ID: {doc['id']}")
            print(f"Title: {doc['title']}")
            print(f"Length: {doc['length']} characters")
            print("-" * 80)
    else:
        print("⚠️  DATABASE IS EMPTY!")
        print("The system can only detect plagiarism against documents already in the database.")
        print("\nTo test plagiarism detection:")
        print("1. Submit a document first (this becomes your reference)")
        print("2. Submit another document to compare against it")
