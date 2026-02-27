from sentence_transformers import SentenceTransformer
from sqlalchemy import text
import os

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def generate_embedding(text_input: str):
    """Convierte texto en una lista de números (vector)."""
    try:
        embedding = model.encode(text_input)
        return embedding.tolist()
    except Exception as e:
        print(f"❌ Error al generar embedding: {e}")
        return None

def search_vector_database(db, query_text, category=None, threshold=0.28, top_k=3):
    """Busca en Postgres usando similitud de coseno."""
    try:
        query_vector = generate_embedding(query_text)
        
        if not query_vector:
            return []

        vector_str = f"[{','.join(map(str, query_vector))}]"

        query_sql = text("""
            SELECT title, content, url, category, 
                   (1 - (embedding <=> :qv)) as similarity
            FROM documents
            WHERE (1 - (embedding <=> :qv)) >= :t
            ORDER BY similarity DESC
            LIMIT :k
        """)
        
        results = db.execute(query_sql, {
            "qv": vector_str, 
            "t": threshold, 
            "k": top_k
        }).fetchall()

        if not results:
            print(f"🔍 Busqué '{query_text}' pero no superó el threshold de {threshold}")
        for r in results:
            print(f"✅ DEBUG: Encontrado '{r.title}' con similitud: {r.similarity:.4f}")
        
        return results

    except Exception as e:
        print(f"❌ Error en búsqueda vectorial: {e}")
        db.rollback() 
        return []