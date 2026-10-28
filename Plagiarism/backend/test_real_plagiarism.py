"""Test with real-world plagiarism example"""
from plagiarism_engine import final_similarity, find_plagiarized_words

print("="*80)
print("REAL-WORLD PLAGIARISM TEST")
print("="*80)

# Original text (from a source)
original = """
Machine learning is a method of data analysis that automates analytical model building. 
It is a branch of artificial intelligence based on the idea that systems can learn from data, 
identify patterns and make decisions with minimal human intervention. Machine learning algorithms 
are trained using large amounts of data and they learn how to perform the task from the data.
"""

# Test 1: Exact copy
copied_exact = """
Machine learning is a method of data analysis that automates analytical model building. 
It is a branch of artificial intelligence based on the idea that systems can learn from data, 
identify patterns and make decisions with minimal human intervention. Machine learning algorithms 
are trained using large amounts of data and they learn how to perform the task from the data.
"""

print("\n1. EXACT COPY (100% plagiarism)")
print("-" * 80)
scores = final_similarity(original, copied_exact)
plagiarized = find_plagiarized_words(original, copied_exact)
print(f"Final Score: {scores['final_score']}%")
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Matching Phrases: {len(plagiarized['matching_phrases'])}")
if plagiarized['matching_phrases']:
    print("Top phrases:")
    for phrase in plagiarized['matching_phrases'][:3]:
        print(f"  - '{phrase}'")

# Test 2: Minor changes (changing a few words)
copied_minor = """
Machine learning is a technique of data analysis that automates analytical model building. 
It is a branch of artificial intelligence based on the concept that systems can learn from data, 
identify patterns and make decisions with minimal human intervention. Machine learning algorithms 
are trained using large amounts of information and they learn how to perform the task from the data.
"""

print("\n2. MINOR CHANGES (90% plagiarism - few words changed)")
print("-" * 80)
scores = final_similarity(original, copied_minor)
plagiarized = find_plagiarized_words(original, copied_minor)
print(f"Final Score: {scores['final_score']}%")
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Matching Phrases: {len(plagiarized['matching_phrases'])}")
if plagiarized['matching_phrases']:
    print("Top phrases:")
    for phrase in plagiarized['matching_phrases'][:3]:
        print(f"  - '{phrase}'")

# Test 3: Sentence reordering
copied_reorder = """
It is a branch of artificial intelligence based on the idea that systems can learn from data, 
identify patterns and make decisions with minimal human intervention. Machine learning is a method 
of data analysis that automates analytical model building. Machine learning algorithms are trained 
using large amounts of data and they learn how to perform the task from the data.
"""

print("\n3. SENTENCE REORDERING (80% plagiarism)")
print("-" * 80)
scores = final_similarity(original, copied_reorder)
plagiarized = find_plagiarized_words(original, copied_reorder)
print(f"Final Score: {scores['final_score']}%")
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Matching Phrases: {len(plagiarized['matching_phrases'])}")
if plagiarized['matching_phrases']:
    print("Top phrases:")
    for phrase in plagiarized['matching_phrases'][:3]:
        print(f"  - '{phrase}'")

# Test 4: Partial copy (50% copied)
copied_partial = """
Machine learning is a method of data analysis that automates analytical model building. 
It is a branch of artificial intelligence. Modern AI systems use various techniques including 
neural networks and deep learning to solve complex problems in computer vision and natural language.
"""

print("\n4. PARTIAL COPY (50% plagiarism)")
print("-" * 80)
scores = final_similarity(original, copied_partial)
plagiarized = find_plagiarized_words(original, copied_partial)
print(f"Final Score: {scores['final_score']}%")
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Matching Phrases: {len(plagiarized['matching_phrases'])}")
if plagiarized['matching_phrases']:
    print("Top phrases:")
    for phrase in plagiarized['matching_phrases'][:3]:
        print(f"  - '{phrase}'")

print("\n" + "="*80)
print("EXPECTED RESULTS:")
print("  1. Exact Copy: Should be 95-100%")
print("  2. Minor Changes: Should be 80-95%")
print("  3. Sentence Reordering: Should be 75-90%")
print("  4. Partial Copy: Should be 40-60%")
print("="*80)
