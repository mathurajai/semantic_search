
def start_frontend():
    import streamlit as st

    # Title of the app
    st.title("Text Input Example")

    # Get user input
    user_input = st.text_input("Enter some text:")

    # Process the input and get a response
    def process_input(input_text):
        response = f"You entered: {input_text}"
        return response

    # Display the response
    if user_input:
        response = process_input(user_input)
        st.write(response)
