from transformers import AutoTokenizer, AutoModelForCausalLM


def generate_text__intel_distilgpt2_wikitext2(input_text, max_length=50, num_return_sequences=1):
    model_directory = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\text2text_generation\models\intel_distilgpt2_wikitext2_saved_model"

    # Load the tokenizer and model from the saved directory
    tokenizer = AutoTokenizer.from_pretrained(model_directory)
    model = AutoModelForCausalLM.from_pretrained(model_directory)

    # Encode the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate output from the model
    outputs = model.generate(input_ids, max_length=max_length, num_return_sequences=num_return_sequences)

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Generated Text:", generated_text)

    return generated_text
