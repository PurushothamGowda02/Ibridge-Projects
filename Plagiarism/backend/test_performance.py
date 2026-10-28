"""Test performance of plagiarism detection"""
import time
from database import get_connection
from plagiarism_engine import top_matches

# Test text
test_text = """
Machine learning is a method of data analysis that automates analytical model building.
It is a branch of artificial intelligence based on the idea that systems can learn from data,
identify patterns and make decisions with minimal human intervention.
"""

print("="*80)
print("PERFORMANCE TEST")
print("="*80)

# Get corpus from database
with get_connection() as conn:
    corpus_rows = conn.execute(
        "SELECT id, title, raw_text FROM documents ORDER BY id ASC"
    ).fetchall()
    corpus = [(row["id"], row["title"], row["raw_text"]) for row in corpus_rows]

print(f"\nDocuments in database: {len(corpus)}")
print(f"Test text length: {len(test_text)} characters")

# Time the comparison
start_time = time.time()
matches = top_matches(test_text, corpus, limit=5)
end_time = time.time()

elapsed = end_time - start_time

print(f"\n⏱️  Time taken: {elapsed:.2f} seconds")
print(f"📊 Matches found: {len(matches)}")

if elapsed > 5:
    print("\n⚠️  WARNING: Detection is slow (>5 seconds)")
    print("   This could be due to:")
    print("   - Large documents in database")
    print("   - Too many documents")
    print("   - Slow computer")
elif elapsed > 2:
    print("\n⚡ Performance is acceptable (2-5 seconds)")
else:
    print("\n✅ Performance is good (<2 seconds)")

print("\n" + "="*80)
