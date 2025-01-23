from app.logging_config import get_logger
from app.backend.item import Item
from sentence_transformers import SentenceTransformer

# Get the logger
logger = get_logger(__name__)

# Load the model from the local directory
model = SentenceTransformer('./app/model/allMiniLML6v2')

def generate_embeddings(sentences):
    
    # Generate embeddings
    embeddings = model.encode(sentences)
    
    items = []
    counter = 0
    # Create a list of Item objects
    for sentence in sentences:      
        items.append(Item(content=sentence, embedding=embeddings[counter].tolist()))
        counter += 1
    
    return items