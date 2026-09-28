"""
Day 2: Knowledge Base Design
Property and FAQ dataset schemas
"""

KNOWLEDGE_BASE_SCHEMA = {
    "properties": {
        "id": "UUID (primary key)",
        "title": "String (e.g., DHA Phase 5, 10 Marla Plot)",
        "type": "Enum (residential/commercial/plot)",
        "status": "Enum (available/sold/rented)",
        "price": "Integer (PKR)",
        "price_per_sqft": "Integer",
        "area_sqft": "Integer",
        "city": "String",
        "area": "String",
        "bedrooms": "Integer",
        "bathrooms": "Integer",
        "developer": "String",
        "project_name": "String",
        "possession_date": "Date",
        "amenities": "JSON array",
        "nearby_schools": "JSON array",
        "nearby_hospitals": "JSON array",
        "payment_plans": "JSON array of {down, installments, monthly}",
        "coordinates": "JSON {lat, lng}"
    },
    "faqs": {
        "id": "UUID",
        "question": "String",
        "answer": "String",
        "category": "Enum (payment_plans, maintenance, schools, hospitals, amenities, investment, legal, possession, utilities, pricing)"
    },
    "brochures": {
        "id": "UUID",
        "property_id": "FK to properties",
        "title": "String",
        "content": "Text (full brochure text)",
        "file_path": "String (PDF location)"
    }
}

if __name__ == "__main__":
    print("Knowledge Base Schema:")
    for table, fields in KNOWLEDGE_BASE_SCHEMA.items():
        print(f"\n{table.upper()}:")
        for field, dtype in fields.items():
            print(f"  - {field}: {dtype}")