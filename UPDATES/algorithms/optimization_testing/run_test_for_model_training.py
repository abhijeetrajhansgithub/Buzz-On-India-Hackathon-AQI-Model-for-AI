from algorithms.optimization_testing.training__without_intel_optimization_model_training import get_time__without_intel_optimization_model_training
from algorithms.optimization_testing.training__with_intel_optimization_model_training import get_time__with_intel_optimization_model_training
import json

result__with_intel = get_time__with_intel_optimization_model_training()
result__without_intel = get_time__without_intel_optimization_model_training()

# Combine results into a new dictionary
final_dict = {}
final_dict.update(result__with_intel)
final_dict.update(result__without_intel)

# Write the combined results to a JSON file
with open('model_training_results.json', 'w') as results_file:
    json.dump(final_dict, results_file, indent=4)

print("Done")

