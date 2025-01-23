from app.logging_config import get_logger
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery, FilterQuery
from app.backend.time_calc import measure_time

# Get the logger
logger = get_logger(__name__)

_item_index = None

def create_index():
    global _item_index
    if _item_index is not None:
        return
    
    _item_index = SearchIndex.from_yaml('./app/backend/redis/items_schema.yml')
    _item_index.connect('redis://localhost:6379')
    _item_index.create(overwrite=True)

create_index()

@measure_time
def cosine_search(item):
    # Perform cosine similarity search
    query = VectorQuery(
        vector=item.embedding,
        vector_field_name='content_embedding',
        return_fields=["content", "vector_distance"],
        num_results=5
    )

    results = _item_index.query(query)
    # Filter results based on distance threshold
    filtered_results = [{'content': result['content'], 'vector_distance': result['vector_distance']} for result in results if float(result['vector_distance']) <= 0.7]
    return filtered_results

@measure_time
def persist_records(items):
    records = [item.to_dict_for_redis() for item in items]
    # Store the record in Redis using RedisVL
    insert_count = _item_index.load(records, id_field='content')
    logger.info(f"Total records inserted {len(insert_count)}")

@measure_time
def get_available_sentences():
    try:
        documents = []
        offset = 0
        page_size = 100  
        while True:
            # Fetch all documents in the index
            query = FilterQuery(return_fields=['content']).paging(offset=offset, num=page_size)
            results = _item_index.query(query)
            if not results:
                break
            # Remove the 'id' field from each result
            cleaned_data = [item['content'] for item in results]
            documents.extend(cleaned_data)
            offset += page_size
        return documents
    except Exception as e:
        logger.error(f"An error occurred: {e}")