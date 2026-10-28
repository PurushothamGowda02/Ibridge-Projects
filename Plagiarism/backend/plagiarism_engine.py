import re
from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9']+", text.lower())


def shingles(text: str, size: int = 5) -> set:
    """Generate word shingles (n-grams) from text"""
    tokens = tokenize(text)
    if len(tokens) < size:
        return {" ".join(tokens)} if tokens else set()
    # Create overlapping shingles
    result = set()
    for i in range(len(tokens) - size + 1):
        result.add(" ".join(tokens[i : i + size]))
    return result


def jaccard_similarity(a: str, b: str) -> float:
    """Calculate Jaccard similarity using word shingles"""
    # Use multiple shingle sizes for better detection
    similarities = []
    
    for size in [3, 4, 5]:  # Check 3, 4, and 5-word sequences
        s1 = shingles(a, size=size)
        s2 = shingles(b, size=size)
        if s1 or s2:
            union = len(s1.union(s2))
            if union > 0:
                intersection = len(s1.intersection(s2))
                similarities.append(intersection / union)
    
    # Return average of all shingle sizes
    return sum(similarities) / len(similarities) if similarities else 0.0


def tfidf_similarity(a: str, b: str) -> float:
    """Calculate TF-IDF cosine similarity between two texts"""
    docs = [clean_text(a), clean_text(b)]
    # Use 1-3 word n-grams for better detection
    # Remove stop_words parameter to catch more similarities
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), min_df=1, max_df=1.0)
    try:
        tfidf = vectorizer.fit_transform(docs)
        similarity = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
        return similarity
    except:
        # Fallback if vectorization fails
        return 0.0


def word_overlap_similarity(a: str, b: str) -> float:
    """Calculate simple word overlap ratio"""
    tokens_a = set(tokenize(a))
    tokens_b = set(tokenize(b))
    
    if not tokens_a or not tokens_b:
        return 0.0
    
    intersection = len(tokens_a.intersection(tokens_b))
    union = len(tokens_a.union(tokens_b))
    
    return intersection / union if union > 0 else 0.0


def final_similarity(a: str, b: str) -> Dict[str, float]:
    """Calculate final similarity score combining multiple methods"""
    tfidf_score = tfidf_similarity(a, b)
    jaccard_score = jaccard_similarity(a, b)
    word_overlap = word_overlap_similarity(a, b)
    
    # Weighted combination: 50% TF-IDF, 30% Jaccard, 20% Word Overlap
    final_score = 0.5 * tfidf_score + 0.3 * jaccard_score + 0.2 * word_overlap
    
    return {
        "tfidf_score": round(tfidf_score * 100, 2),
        "jaccard_score": round(jaccard_score * 100, 2),
        "final_score": round(final_score * 100, 2),
    }


def verdict(score: float) -> str:
    if score >= 75:
        return "High plagiarism risk"
    if score >= 45:
        return "Moderate plagiarism risk"
    return "Low plagiarism risk"


def find_matching_phrases(input_text: str, reference_text: str, min_words: int = 3) -> List[str]:
    """
    Find matching phrases between input and reference text.
    Returns list of unique matching phrases with at least min_words length.
    """
    input_tokens = tokenize(input_text)
    reference_tokens = tokenize(reference_text)
    
    matching_phrases = []
    used_positions = set()  # Track positions already covered
    
    # Check for matching sequences of different lengths (from longest to shortest)
    max_length = min(len(input_tokens), len(reference_tokens), 20)  # Increased to 20
    
    for length in range(max_length, min_words - 1, -1):
        for i in range(len(input_tokens) - length + 1):
            # Skip if this position is already part of a longer match
            if any(pos in used_positions for pos in range(i, i + length)):
                continue
                
            phrase = input_tokens[i:i + length]
            phrase_str = " ".join(phrase)
            
            # Check if this phrase exists in reference text
            for j in range(len(reference_tokens) - length + 1):
                if phrase == reference_tokens[j:j + length]:
                    # Avoid adding if it's a substring of existing phrase
                    is_duplicate = any(phrase_str in existing or existing in phrase_str 
                                      for existing in matching_phrases)
                    if not is_duplicate:
                        matching_phrases.append(phrase_str)
                        # Mark these positions as used
                        for pos in range(i, i + length):
                            used_positions.add(pos)
                    break
    
    return matching_phrases


def find_plagiarized_words(input_text: str, reference_text: str) -> Dict:
    """
    Identify specific words and phrases that are plagiarized.
    Returns matching phrases and individual common words.
    """
    # Find matching phrases (3+ words) - reduced from 4
    matching_phrases = find_matching_phrases(input_text, reference_text, min_words=3)
    
    # Find matching shingles (4-word sequences for better detection)
    input_shingles = shingles(input_text, size=4)
    reference_shingles = shingles(reference_text, size=4)
    common_shingles = list(input_shingles.intersection(reference_shingles))
    
    # Find individual common words (excluding common stop words)
    input_tokens = set(tokenize(input_text))
    reference_tokens = set(tokenize(reference_text))
    common_words = list(input_tokens.intersection(reference_tokens))
    
    # Reduced stop words list - keep more meaningful words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                  'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                  'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
                  'these', 'those', 'it', 'its', 'they', 'their', 'them'}
    
    common_words = [w for w in common_words if w not in stop_words and len(w) > 2]
    
    return {
        "matching_phrases": matching_phrases[:8],  # Increased to 8
        "common_shingles": common_shingles[:5],    # Increased to 5
        "common_words": sorted(common_words)[:15],  # Increased to 15
        "total_matching_phrases": len(matching_phrases),
        "total_common_words": len(common_words)
    }


def get_text_snippet(text: str, max_length: int = 150) -> str:
    """Get a preview snippet of text"""
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."


def find_matching_context(input_text: str, reference_text: str, phrase: str) -> str:
    """Find the context around a matching phrase in the reference text"""
    ref_lower = reference_text.lower()
    phrase_lower = phrase.lower()
    
    pos = ref_lower.find(phrase_lower)
    if pos == -1:
        return phrase
    
    # Get 50 chars before and after
    start = max(0, pos - 50)
    end = min(len(reference_text), pos + len(phrase) + 50)
    
    snippet = reference_text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(reference_text):
        snippet = snippet + "..."
    
    return snippet


def top_matches(input_text: str, corpus: List[Tuple[int, str, str]], limit: int = 5):
    results = []
    seen_titles = set()  # Track titles to avoid duplicates
    
    for doc_id, title, text in corpus:
        # Skip duplicate titles (case-insensitive)
        title_key = title.lower().strip()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        
        scores = final_similarity(input_text, text)
        plagiarized_content = find_plagiarized_words(input_text, text)
        
        # Get document preview
        doc_preview = get_text_snippet(text, max_length=200)
        
        # Get context for first matching phrase if available
        matching_context = None
        if plagiarized_content["matching_phrases"]:
            first_phrase = plagiarized_content["matching_phrases"][0]
            matching_context = find_matching_context(input_text, text, first_phrase)
        
        results.append(
            {
                "doc_id": doc_id,
                "title": title,
                "final_score": scores["final_score"],
                "tfidf_score": scores["tfidf_score"],
                "jaccard_score": scores["jaccard_score"],
                "verdict": verdict(scores["final_score"]),
                "plagiarized_words": plagiarized_content,
                "document_preview": doc_preview,
                "matching_context": matching_context
            }
        )
    
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results[:limit]

