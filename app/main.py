from logging_config import get_logger
from backend.config_loader import load_all_configs
from backend.embeddings_generator import generate_embeddings
from backend.persistence_postgres import persist_records, cosine_search
from backend.item import Item

# Get the logger
logger = get_logger(__name__)

sentence1 = "The weather today is better than yesterday."
sentence2 = "She loves to paint landscapes."
sentence3 = "The application crashes when I try to upload a file."
sentence4 = "The alerts are not being sent to my email."
sentence5 = "The translation feature is planned for next sprint."
sentence6 = "The application crash related to logging is getting fixed in sprint4"

example_sentences = [
    sentence1,
    sentence2,
    sentence3,
    sentence4,
    sentence5,
    sentence6,
    "Yesterday's weather was rainy.",
    "This movie is more interesting than the last one.",
    "Despite the heavy rain, the event continued as planned.",
    "Although he was tired, he finished his homework before going to bed.",
    "What time does the meeting start?",
    "It's raining cats and dogs.",
    "He kicked the bucket."
]

test_sentences = {
    "The sun rises in the east.": sentence1,
    "She enjoys reading books.": sentence2,
    "The software freezes during the login process.": sentence3,
    "There is a bug that causes the app to close unexpectedly.": [sentence3, sentence6],
    "I am experiencing issues with the notification settings.": sentence4,
    "The app should support multiple languages, which would be convenient.": sentence5
}

def main():
    
    # first log that applicatio is starting
    logger.info('starting the app')
    
    # load all the config at startup
    load_all_configs("./app/")
    
    # convert example sentences into embeddings
    items = generate_embeddings(sentences=example_sentences)
    
    # persist the items
    persist_records(items)
    
    # search similar sentences
    for test_sentence_key, test_sentence_values in test_sentences.items():
        search_cosine_similar([test_sentence_key])
        
                          
def search_cosine_similar(query):
    query_embedding = generate_embeddings(query)[0].embedding
    results = cosine_search(Item(content=query, embedding=query_embedding))
    logger.info(f"For {query} the cosine similarity results are {results}")
    return results
    
if __name__ == "__main__":
    main()