from transformers import T5Tokenizer, T5ForConditionalGeneration


def generate_text__google_flan_t5_large(prompt: str):
    # Step 1: Load the tokenizer and model
    model_name = "google/flan-t5-large"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # Tokenize the input prompt and prepare input for the model
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate text using the model
    output_sequences = model.generate(
        inputs.input_ids,
        max_length=1000,  # Maximum length of generated text
        num_return_sequences=1,  # Number of sequences to generate
        no_repeat_ngram_size=2,  # Avoid repeating n-grams
        num_beams=15,  # Beam search for better results
        temperature=0.2,  # Adjust temperature for randomness (lower is less random)
        top_p=0.9,  # Top-p (nucleus) sampling for diversity
        early_stopping=False  # Generate text until max_length is reached
    )

    # Decode the generated text
    generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
    print("Generated Text:\n", generated_text)

    return generated_text

# # Example usage
# print(generate_text("What are pollutants?"))
