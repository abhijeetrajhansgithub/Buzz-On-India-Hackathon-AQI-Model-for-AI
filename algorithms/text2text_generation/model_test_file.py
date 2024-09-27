from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Path to the unzipped model directory
model_directory = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\text2text_generation\models\fine_tuned_distilgpt2_model_intel_distilgpt2_wikitext2_saved_model"
# Load the tokenizer and model from the saved directory
tokenizer = AutoTokenizer.from_pretrained(model_directory)
model = AutoModelForCausalLM.from_pretrained(model_directory)

# Example usage: Generate text
input_text = "Tell me about the AQI. it is"
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate output from the model
outputs = model.generate(input_ids, max_length=120, num_return_sequences=1)
print(outputs)

# Decode and print the generated text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Generated Text:", generated_text)
