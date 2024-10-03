from algorithms.optimization_testing.prediction__with_intel_optimization_model_training import intel__calculate_air_quality_manually_final_suggested_verdict
from algorithms.optimization_testing.prediction__without_intel_optimization_model_training import calculate_air_quality_manually_final_suggested_verdict
import json

# Call the functions to get results
result__with_intel = intel__calculate_air_quality_manually_final_suggested_verdict(4000, 30, 45, 61, 44, 22)
result__without_intel = calculate_air_quality_manually_final_suggested_verdict(4000, 30, 45, 61, 44, 22)

# Combine results into a new dictionary
final_dict = {}
final_dict.update(result__with_intel)
final_dict.update(result__without_intel)

# Write the combined results to a JSON file
with open('air_quality_results.json', 'w') as results_file:
    json.dump(final_dict, results_file, indent=4)
