from mm_algorithms.mm_model_1.models.prediction.gradient_boosting_regression_model.gradient_boosting_regression_model import get_multimodal_model_1__gradient_boosting__calculate_air_quality__POWAC
from mm_algorithms.mm_model_1.models.prediction.decision_tree_regression_model.decision_tree_regression_model import get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC
from mm_algorithms.mm_model_1.models.prediction.random_forest_regression_model.random_forest_regression_model import get_multimodal_model_1__random_forest__calculate_air_quality__POWAC


def weighting_nd(weights=(0.3, 0.5, 0.2)):
    # Ensure weights sum to 1
    assert len(weights) == 3, "Weights should be a list of three values."
    assert sum(weights) == 1, "Weights must sum to 1."

    # Get predictions from each model
    prediction_1 = get_multimodal_model_1__gradient_boosting__calculate_air_quality__POWAC()
    print("PREDICTION 1: ", prediction_1)
    prediction_2 = get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC()
    print("PREDICTION 2: ", prediction_2)
    prediction_3 = get_multimodal_model_1__random_forest__calculate_air_quality__POWAC()
    print("PREDICTION 3: ", prediction_3)

    # Check if any prediction is None
    if prediction_1 is None or prediction_2 is None or prediction_3 is None:
        raise ValueError("One or more model predictions returned None. Check the models.")

    # Weighted sum of predictions
    weighted_prediction = (weights[0] * prediction_1) + (weights[1] * prediction_2) + (weights[2] * prediction_3)

    return weighted_prediction


print(weighting_nd(weights=(0.3, 0.5, 0.2)))
