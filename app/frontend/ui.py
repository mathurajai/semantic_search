from app.logging_config import get_logger
from app.backend.processor import search_cosine_similar, get_available_sentences


# Get the logger
logger = get_logger(__name__)

def start_frontend():

    logger.info("Starting the app")
    import streamlit as st

    # Title of the app
    st.title("Semantic Search")

    col1, col2 = st.columns(2)

    #with col1:
        # Get user input
    user_input = col1.text_input("Enter a sentence:")

    #with col2: 
    db_column_values = get_available_sentences()
    if db_column_values: 
        col2.write("Available sentences:") 
        for value in db_column_values: 
            col2.write(value)

    # Display the response
    if user_input:
        response = process_input(user_input)
        col1.write(response)

# Process the input and get a response
def process_input(input_text):
    response = [f"You entered: {input_text}"]
    response.append(search_cosine_similar([input_text]))
    return response  
    
if __name__ == "__main__":
    start_frontend()