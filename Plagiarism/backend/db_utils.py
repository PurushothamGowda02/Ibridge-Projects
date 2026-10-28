"""Database utility functions for cleaning and managing documents"""
import sqlite3
from database import get_connection


def remove_duplicate_documents():
    """Remove duplicate documents based on title and keep the oldest one"""
    with get_connection() as conn:
        # Find duplicates
        duplicates = conn.execute("""
            SELECT title, MIN(id) as keep_id, GROUP_CONCAT(id) as all_ids
            FROM documents
            GROUP BY LOWER(TRIM(title))
            HAVING COUNT(*) > 1
        """).fetchall()
        
        removed_count = 0
        for dup in duplicates:
            all_ids = [int(x) for x in dup['all_ids'].split(',')]
            keep_id = dup['keep_id']
            remove_ids = [x for x in all_ids if x != keep_id]
            
            if remove_ids:
                placeholders = ','.join('?' * len(remove_ids))
                # Delete comparisons first (foreign key constraint)
                conn.execute(f"DELETE FROM comparisons WHERE source_doc_id IN ({placeholders})", remove_ids)
                conn.execute(f"DELETE FROM comparisons WHERE compared_doc_id IN ({placeholders})", remove_ids)
                # Delete documents
                conn.execute(f"DELETE FROM documents WHERE id IN ({placeholders})", remove_ids)
                removed_count += len(remove_ids)
        
        conn.commit()
        return removed_count


def get_document_stats():
    """Get statistics about documents in database"""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) as count FROM documents").fetchone()['count']
        
        # Find potential duplicates
        duplicates = conn.execute("""
            SELECT COUNT(*) as dup_count
            FROM (
                SELECT title, COUNT(*) as cnt
                FROM documents
                GROUP BY LOWER(TRIM(title))
                HAVING cnt > 1
            )
        """).fetchone()['dup_count']
        
        return {
            'total_documents': total,
            'duplicate_titles': duplicates
        }


if __name__ == "__main__":
    print("Database Statistics:")
    stats = get_document_stats()
    print(f"Total documents: {stats['total_documents']}")
    print(f"Duplicate titles: {stats['duplicate_titles']}")
    
    if stats['duplicate_titles'] > 0:
        print("\nRemoving duplicates...")
        removed = remove_duplicate_documents()
        print(f"Removed {removed} duplicate documents")
        
        print("\nUpdated Statistics:")
        stats = get_document_stats()
        print(f"Total documents: {stats['total_documents']}")
        print(f"Duplicate titles: {stats['duplicate_titles']}")
