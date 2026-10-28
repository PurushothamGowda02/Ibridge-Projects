"""Test plagiarism detection algorithms"""
from plagiarism_engine import (
    tfidf_similarity, 
    jaccard_similarity, 
    final_similarity,
    find_matching_phrases,
    find_plagiarized_words
)

# Test cases
print("=" * 80)
print("PLAGIARISM DETECTION TEST")
print("=" * 80)

# Test 1: Exact copy
text1 = "This is a test document about machine learning and artificial intelligence."
text2 = "This is a test document about machine learning and artificial intelligence."

print("\n1. EXACT COPY TEST")
print(f"Text 1: {text1}")
print(f"Text 2: {text2}")
scores = final_similarity(text1, text2)
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Final: {scores['final_score']}%")
print(f"Expected: ~100%")

# Test 2: High plagiarism (80% same)
text3 = "Machine learning is a subset of artificial intelligence that enables computers to learn from data."
text4 = "Machine learning is a subset of artificial intelligence that allows systems to learn from information."

print("\n2. HIGH PLAGIARISM TEST (80% similar)")
print(f"Text 1: {text3}")
print(f"Text 2: {text4}")
scores = final_similarity(text3, text4)
phrases = find_matching_phrases(text3, text4, min_words=3)
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Final: {scores['final_score']}%")
print(f"Matching phrases: {phrases}")
print(f"Expected: 70-90%")

# Test 3: Moderate plagiarism (50% same)
text5 = "Python is a popular programming language used for data science and web development."
text6 = "Python is widely used in data science. It is also popular for creating web applications."

print("\n3. MODERATE PLAGIARISM TEST (50% similar)")
print(f"Text 1: {text5}")
print(f"Text 2: {text6}")
scores = final_similarity(text5, text6)
phrases = find_matching_phrases(text5, text6, min_words=3)
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Final: {scores['final_score']}%")
print(f"Matching phrases: {phrases}")
print(f"Expected: 40-60%")

# Test 4: Low plagiarism (different content, same topic)
text7 = "Deep learning uses neural networks with multiple layers to process complex patterns."
text8 = "Artificial intelligence helps computers make decisions based on data analysis."

print("\n4. LOW PLAGIARISM TEST (same topic, different content)")
print(f"Text 1: {text7}")
print(f"Text 2: {text8}")
scores = final_similarity(text7, text8)
phrases = find_matching_phrases(text7, text8, min_words=3)
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Final: {scores['final_score']}%")
print(f"Matching phrases: {phrases}")
print(f"Expected: 10-30%")

# Test 5: No plagiarism (completely different)
text9 = "The weather today is sunny and warm with clear blue skies."
text10 = "Machine learning algorithms require large datasets for training purposes."

print("\n5. NO PLAGIARISM TEST (completely different)")
print(f"Text 1: {text9}")
print(f"Text 2: {text10}")
scores = final_similarity(text9, text10)
phrases = find_matching_phrases(text9, text10, min_words=3)
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Final: {scores['final_score']}%")
print(f"Matching phrases: {phrases}")
print(f"Expected: 0-10%")

# Test 6: Paraphrased content
text11 = "Students often struggle with understanding complex mathematical concepts in their coursework."
text12 = "Many learners find it difficult to grasp complicated math ideas during their studies."

print("\n6. PARAPHRASED CONTENT TEST")
print(f"Text 1: {text11}")
print(f"Text 2: {text12}")
scores = final_similarity(text11, text12)
phrases = find_matching_phrases(text11, text12, min_words=3)
plagiarized = find_plagiarized_words(text11, text12)
print(f"TF-IDF: {scores['tfidf_score']}%")
print(f"Jaccard: {scores['jaccard_score']}%")
print(f"Final: {scores['final_score']}%")
print(f"Matching phrases: {phrases}")
print(f"Common words: {plagiarized['common_words']}")
print(f"Expected: 20-40%")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
