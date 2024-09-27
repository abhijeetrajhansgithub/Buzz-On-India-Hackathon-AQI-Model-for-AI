# Load the model and tokenizer directly from Hugging Face Hub
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer for the model
tokenizer = AutoTokenizer.from_pretrained("Intel/fid_flan_t5_base_nq")

# Load the model
model = AutoModelForSeq2SeqLM.from_pretrained("Intel/fid_flan_t5_base_nq")

# Example usage: Tokenize and generate text
input_text = "What is the capital of France?"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate response from the model
outputs = model.generate(**inputs)

# Decode the generated tokens to a human-readable string
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(generated_text)
