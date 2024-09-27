import transformers
import torch

# Load the model and tokenizer once, outside the function
model_name = 'Intel/neural-chat-7b-v3-3'
model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)


def generate_response(system_input, user_input):
    # Format the input prompt
    prompt = f"### System:\n{system_input}\n### User:\n{user_input}\n### Assistant:\n"

    # Tokenize the prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=False)

    # Generate response with no gradient calculation (faster inference)
    with torch.no_grad():
        outputs = model.generate(inputs, max_new_tokens=200, num_return_sequences=1,
                                 early_stopping=True)

    # Decode and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("### Assistant:\n")[-1]


# Example usage
system_input = ("You are a math expert assistant. Your mission is to help users "
                "understand and solve various math problems. Provide step-by-step "
                "solutions, explain reasonings, and give the correct answer.")
user_input = "calculate 100 + 520 + 60"
response = generate_response(system_input, user_input)
print(response)
