"""Memory System - Vector-based storage and retrieval for conversations and facts"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import uuid
import numpy as np
from dataclasses import dataclass, asdict
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

# ChromaDB is optional - only import if available
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None


@dataclass
class ConversationEntry:
    """Represents a single conversation exchange"""
    id: str
    timestamp: datetime
    user_input: str
    assistant_response: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


@dataclass
class MemoryFact:
    """Represents a stored fact or piece of information"""
    id: str
    content: str
    category: str
    timestamp: datetime
    metadata: Dict[str, Any]
    embedding: List[float]


class MemorySystem:
    """
    Manages conversation history and fact storage using FAISS or ChromaDB vector store
    with sentence-transformers embeddings for semantic search.
    """
    
    def __init__(
        self,
        vector_store_type: str = "faiss",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        dimension: int = 384,
        persist_directory: Optional[str] = None
    ):
        """
        Initialize the Memory System with specified vector store.
        
        Args:
            vector_store_type: Type of vector store to use ('faiss' or 'chromadb')
            embedding_model: Name of the sentence-transformers model to use
            dimension: Dimension of the embedding vectors (384 for all-MiniLM-L6-v2)
            persist_directory: Directory for persistent storage (ChromaDB only)
        """
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.dimension = dimension
        self.vector_store_type = vector_store_type.lower()
        self.persist_directory = persist_directory
        
        # Initialize based on vector store type
        if self.vector_store_type == "faiss":
            self._init_faiss()
        elif self.vector_store_type == "chromadb":
            self._init_chromadb()
        else:
            raise ValueError(f"Unsupported vector store type: {vector_store_type}. Use 'faiss' or 'chromadb'.")
    
    def _init_faiss(self):
        """Initialize FAISS vector store."""
        # Initialize FAISS indices for conversations and facts
        self.conversation_index = faiss.IndexFlatL2(self.dimension)
        self.fact_index = faiss.IndexFlatL2(self.dimension)
        
        # Storage for conversation entries and facts
        self.conversations: List[ConversationEntry] = []
        self.facts: List[MemoryFact] = []
        
        # Mapping from FAISS index position to entry ID
        self.conversation_id_map: List[str] = []
        self.fact_id_map: List[str] = []
    
    def _init_chromadb(self):
        """Initialize ChromaDB vector store."""
        if not CHROMADB_AVAILABLE:
            raise ImportError(
                "ChromaDB is not installed. Install it with: pip install chromadb\n"
                "Note: ChromaDB requires Microsoft Visual C++ 14.0 or greater on Windows."
            )
        
        # Set up persistence directory
        if self.persist_directory:
            persist_path = Path(self.persist_directory)
            persist_path.mkdir(parents=True, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=str(persist_path))
        else:
            # Use in-memory client if no persistence directory specified
            self.chroma_client = chromadb.Client()
        
        # Create or get collections for conversations and facts
        self.conversation_collection = self.chroma_client.get_or_create_collection(
            name="conversations",
            metadata={"hnsw:space": "l2"}
        )
        self.fact_collection = self.chroma_client.get_or_create_collection(
            name="facts",
            metadata={"hnsw:space": "l2"}
        )
        
        # In-memory storage for quick access (ChromaDB stores data internally)
        self.conversations: List[ConversationEntry] = []
        self.facts: List[MemoryFact] = []
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def store_conversation(
        self,
        user_input: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a conversation exchange with embeddings.
        
        Args:
            user_input: The user's input text
            assistant_response: The assistant's response text
            metadata: Optional metadata dictionary
            
        Returns:
            The ID of the stored conversation entry
        """
        if metadata is None:
            metadata = {}
        
        # Generate unique ID
        entry_id = str(uuid.uuid4())
        
        # Create combined text for embedding (user input + response)
        combined_text = f"{user_input} {assistant_response}"
        embedding = self._generate_embedding(combined_text)
        
        # Create conversation entry
        entry = ConversationEntry(
            id=entry_id,
            timestamp=datetime.now(),
            user_input=user_input,
            assistant_response=assistant_response,
            metadata=metadata,
            embedding=embedding
        )
        
        # Store in list
        self.conversations.append(entry)
        
        # Store in vector store
        if self.vector_store_type == "faiss":
            # Add to FAISS index
            embedding_array = np.array([embedding], dtype=np.float32)
            self.conversation_index.add(embedding_array)
            self.conversation_id_map.append(entry_id)
        elif self.vector_store_type == "chromadb":
            # Add to ChromaDB collection
            self.conversation_collection.add(
                ids=[entry_id],
                embeddings=[embedding],
                documents=[combined_text],
                metadatas=[{
                    "user_input": user_input,
                    "assistant_response": assistant_response,
                    "timestamp": entry.timestamp.isoformat(),
                    **metadata
                }]
            )
        
        return entry_id

    def store_fact(
        self,
        fact: str,
        category: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a fact with metadata and embeddings.
        
        Args:
            fact: The fact content to store
            category: Category of the fact (e.g., 'preference', 'personal', 'general')
            metadata: Optional metadata dictionary
            
        Returns:
            The ID of the stored fact
        """
        if metadata is None:
            metadata = {}
        
        # Generate unique ID
        fact_id = str(uuid.uuid4())
        
        # Generate embedding
        embedding = self._generate_embedding(fact)
        
        # Create fact entry
        fact_entry = MemoryFact(
            id=fact_id,
            content=fact,
            category=category,
            timestamp=datetime.now(),
            metadata=metadata,
            embedding=embedding
        )
        
        # Store in list
        self.facts.append(fact_entry)
        
        # Store in vector store
        if self.vector_store_type == "faiss":
            # Add to FAISS index
            embedding_array = np.array([embedding], dtype=np.float32)
            self.fact_index.add(embedding_array)
            self.fact_id_map.append(fact_id)
        elif self.vector_store_type == "chromadb":
            # Add to ChromaDB collection
            self.fact_collection.add(
                ids=[fact_id],
                embeddings=[embedding],
                documents=[fact],
                metadatas=[{
                    "category": category,
                    "timestamp": fact_entry.timestamp.isoformat(),
                    **metadata
                }]
            )
        
        return fact_id
    
    def retrieve_relevant_memories(
        self,
        query: str,
        k: int = 5,
        include_conversations: bool = True,
        include_facts: bool = True
    ) -> List[Tuple[Any, float]]:
        """
        Retrieve relevant memories based on semantic similarity.
        
        Args:
            query: The query text to search for
            k: Number of results to return
            include_conversations: Whether to search conversations
            include_facts: Whether to search facts
            
        Returns:
            List of tuples (memory_entry, similarity_score) sorted by relevance
        """
        results = []
        
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        if self.vector_store_type == "faiss":
            results = self._retrieve_faiss(query_embedding, k, include_conversations, include_facts)
        elif self.vector_store_type == "chromadb":
            results = self._retrieve_chromadb(query_embedding, k, include_conversations, include_facts)
        
        # Sort by similarity score (descending) and return top k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def _retrieve_faiss(
        self,
        query_embedding: List[float],
        k: int,
        include_conversations: bool,
        include_facts: bool
    ) -> List[Tuple[Any, float]]:
        """Retrieve memories using FAISS backend."""
        results = []
        query_array = np.array([query_embedding], dtype=np.float32)
        
        # Search conversations
        if include_conversations and self.conversation_index.ntotal > 0:
            # FAISS returns L2 distances, we need to convert to similarity scores
            distances, indices = self.conversation_index.search(query_array, min(k, self.conversation_index.ntotal))
            
            for dist, idx in zip(distances[0], indices[0]):
                if idx != -1:  # Valid index
                    entry_id = self.conversation_id_map[idx]
                    entry = next((c for c in self.conversations if c.id == entry_id), None)
                    if entry:
                        # Convert L2 distance to similarity score (inverse relationship)
                        # Using exponential decay: similarity = exp(-distance)
                        similarity = np.exp(-dist)
                        results.append((entry, float(similarity)))
        
        # Search facts
        if include_facts and self.fact_index.ntotal > 0:
            distances, indices = self.fact_index.search(query_array, min(k, self.fact_index.ntotal))
            
            for dist, idx in zip(distances[0], indices[0]):
                if idx != -1:  # Valid index
                    fact_id = self.fact_id_map[idx]
                    fact = next((f for f in self.facts if f.id == fact_id), None)
                    if fact:
                        # Convert L2 distance to similarity score
                        similarity = np.exp(-dist)
                        results.append((fact, float(similarity)))
        
        return results
    
    def _retrieve_chromadb(
        self,
        query_embedding: List[float],
        k: int,
        include_conversations: bool,
        include_facts: bool
    ) -> List[Tuple[Any, float]]:
        """Retrieve memories using ChromaDB backend."""
        results = []
        
        # Search conversations
        if include_conversations and self.conversation_collection.count() > 0:
            conv_results = self.conversation_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, self.conversation_collection.count())
            )
            
            if conv_results['ids'] and len(conv_results['ids'][0]) > 0:
                for idx, (entry_id, distance) in enumerate(zip(conv_results['ids'][0], conv_results['distances'][0])):
                    # Find the conversation entry
                    entry = next((c for c in self.conversations if c.id == entry_id), None)
                    if entry:
                        # Convert L2 distance to similarity score
                        similarity = np.exp(-distance)
                        results.append((entry, float(similarity)))
        
        # Search facts
        if include_facts and self.fact_collection.count() > 0:
            fact_results = self.fact_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, self.fact_collection.count())
            )
            
            if fact_results['ids'] and len(fact_results['ids'][0]) > 0:
                for idx, (fact_id, distance) in enumerate(zip(fact_results['ids'][0], fact_results['distances'][0])):
                    # Find the fact entry
                    fact = next((f for f in self.facts if f.id == fact_id), None)
                    if fact:
                        # Convert L2 distance to similarity score
                        similarity = np.exp(-distance)
                        results.append((fact, float(similarity)))
        
        return results
    
    def get_conversation_history(self, limit: int = 10) -> List[ConversationEntry]:
        """
        Retrieve recent conversation history.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of ConversationEntry objects, most recent first
        """
        # Sort by timestamp descending and return limited results
        sorted_conversations = sorted(
            self.conversations,
            key=lambda x: x.timestamp,
            reverse=True
        )
        return sorted_conversations[:limit]
    
    def get_all_facts(self, category: Optional[str] = None) -> List[MemoryFact]:
        """
        Retrieve all stored facts, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of MemoryFact objects
        """
        if category:
            return [f for f in self.facts if f.category == category]
        return self.facts.copy()
    
    def clear_conversations(self):
        """Clear all stored conversations."""
        self.conversations.clear()
        
        if self.vector_store_type == "faiss":
            self.conversation_id_map.clear()
            self.conversation_index = faiss.IndexFlatL2(self.dimension)
        elif self.vector_store_type == "chromadb":
            # Delete and recreate the collection
            self.chroma_client.delete_collection(name="conversations")
            self.conversation_collection = self.chroma_client.get_or_create_collection(
                name="conversations",
                metadata={"hnsw:space": "l2"}
            )
    
    def clear_facts(self):
        """Clear all stored facts."""
        self.facts.clear()
        
        if self.vector_store_type == "faiss":
            self.fact_id_map.clear()
            self.fact_index = faiss.IndexFlatL2(self.dimension)
        elif self.vector_store_type == "chromadb":
            # Delete and recreate the collection
            self.chroma_client.delete_collection(name="facts")
            self.fact_collection = self.chroma_client.get_or_create_collection(
                name="facts",
                metadata={"hnsw:space": "l2"}
            )
    
    def clear_all(self):
        """Clear all stored data."""
        self.clear_conversations()
        self.clear_facts()
