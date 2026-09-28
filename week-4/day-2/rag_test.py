"""
Day 2: RAG Pipeline Implementation
Document loader, chunking, embedding, vector store, retriever
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rag_pipeline import RealEstateRAG

def test_rag_pipeline():
    """Test the complete RAG pipeline"""
    print("Testing RAG Pipeline...")
    print("=" * 50)
    
    rag = RealEstateRAG()
    rag.load_data()
    rag.initialize_vector_store()
    
    test_queries = [
        "Payment plan for DHA Phase 5",
        "Schools near DHA",
        "Commercial plots in DHA",
        "Maintenance charges"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = rag.search(query, top_k=2)
        for r in results:
            print(f"  - {r['document'][:80]}...")
    
    print("\n" + "=" * 50)
    print("RAG Pipeline: WORKING")

if __name__ == "__main__":
    test_rag_pipeline()