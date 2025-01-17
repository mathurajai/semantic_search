def load_one_time():
    from transformers import AutoTokenizer, AutoModel
    from sentence_transformers import SentenceTransformer
    
    # Specify the model name
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    # Download and save the model locally
    model = SentenceTransformer(model_name)
    model.save('./app/model/allMiniLML6v2')
    
    # Download and save the model and tokenizer locally
    #tokenizer = AutoTokenizer.from_pretrained(model_name)
    #model = AutoModel.from_pretrained(model_name)

    # Save the tokenizer and model
    #tokenizer.save_pretrained('./app/model/allMiniLML6v2')
    #model.save_pretrained('./app/model/allMiniLML6v2')

if __name__ == "__main__":
    load_one_time()