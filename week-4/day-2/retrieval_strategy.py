"""
Day 2: Structured vs Semantic Retrieval
Justification for split and implementation
"""

RETRIEVAL_SPLIT = {
    "structured_sql": {
        "use_for": ["price", "availability", "size", "agent_name", "bedrooms", "bathrooms"],
        "why": "Exact numeric/filterable data. SQL is faster and more accurate for structured queries.",
        "implementation": "SQLite queries with WHERE clauses"
    },
    "semantic_vector": {
        "use_for": ["brochures", "descriptions", "FAQs", "amenities", "neighborhood info"],
        "why": "Text-based answers need fuzzy matching. Vector search finds semantically similar content.",
        "implementation": "ChromaDB with embeddings"
    }
}

if __name__ == "__main__":
    print("Retrieval Strategy:")
    for method, details in RETRIEVAL_SPLIT.items():
        print(f"\n{method.upper()}:")
        print(f"  Use for: {details['use_for']}")
        print(f"  Why: {details['why']}")
        print(f"  Implementation: {details['implementation']}")