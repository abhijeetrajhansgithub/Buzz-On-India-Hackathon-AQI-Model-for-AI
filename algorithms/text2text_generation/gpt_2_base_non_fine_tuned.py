from transformers import pipeline, set_seed


def generate_text__gpt2_base_non_fine_tuned(prompt, model_name='gpt2', seed=42, max_length=200, num_return_sequences=5):
    """
    Generates text based on the given prompt using a specified model.

    Args:
    prompt (str): The input text for generation.
    model_name (str): The name of the model to use. Default is 'gpt2'.
    seed (int): Random seed for reproducibility. Default is 42.
    max_length (int): Maximum length of the generated text. Default is 500.
    num_return_sequences (int): Number of sequences to generate. Default is 5.

    Returns:
    list: A list of generated text sequences.
    """
    # Load text generation pipeline and set random seed
    generator = pipeline('text-generation', model=model_name, pad_token_id=50256)
    set_seed(seed)

    # Generate text based on the prompt
    outputs = generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences, truncation=True)

    # Extract and return the generated text from the output dictionaries
    generated_texts = [output['generated_text'] for output in outputs]

    return " ".join(generated_texts)



