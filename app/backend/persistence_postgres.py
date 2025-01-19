from app.logging_config import get_logger
import psycopg2
from app.backend.pool_postgres import get_connection, release_connection

# Get the logger
logger = get_logger(__name__)
sentences = None

def get_available_sentences():
    global sentences
    if sentences is not None:
        return sentences
    
    sentences = []
    conn = None
    try:
        # Get a connection from the pool
        conn = get_connection()
        cursor = conn.cursor()

        # Define your query 
        query = "SELECT content FROM items" 
        # Execute the query 
        cursor.execute(query) 
        # Fetch the results 
        results = cursor.fetchall()
        # Collect the results 
        for row in results:
            sentences.append(row[0])
        
        logger.info(f"{len(sentences)} sentence(s) collected from db")
        return sentences
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error while querying sentences: {error}")
    finally:
        # Release the connection back to the pool
        if conn:
            cursor.close()
            release_connection(conn)

def persist_records(items):
    conn = None
    try:
        # Get a connection from the pool
        conn = get_connection()
        cursor = conn.cursor()

        # Insert multiple records into the table with ON CONFLICT DO NOTHING
        insert_query = """
        INSERT INTO items (content, embedding) 
        VALUES (%s, %s) 
        ON CONFLICT (content) DO NOTHING
        """
        
        records = [item.to_tuple() for item in items]
        cursor.executemany(insert_query, records)

        # Get the number of records inserted
        inserted_records = cursor.rowcount
        
        # Commit the transaction
        conn.commit()
        logger.info(f"{inserted_records} Record(s) inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error while inserting: {error}")
        if conn:
            conn.rollback()
    finally:
        # Release the connection back to the pool
        if conn:
            cursor.close()
            release_connection(conn)

def cosine_search(item):
    # Get a connection from the pool
    conn = get_connection()
    cursor = conn.cursor()
    # Perform a cosine similarity search
    try:
        cursor.execute(
            """SELECT id, content, (embedding <=> %s::vector) AS cosine_similarity
               FROM items
               ORDER BY cosine_similarity LIMIT 5""",
            (item.embedding,)
        )

        # Fetch the similar results
        results = []
        for row in cursor.fetchall():
            # Only add those that are above threshold
            if row[2] < 0.7:
                results.append(f"CONTENT: {row[1]}, Cosine Similarity: {row[2]}")
        
        return results
    
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error while querying sentences: {error}")
    finally:
        # Close communication with the PostgreSQL database server
        cursor.close()
        release_connection(conn)