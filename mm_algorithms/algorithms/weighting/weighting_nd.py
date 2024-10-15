from mm_algorithms.mm_model_1.models.prediction.gradient_boosting_regression_model.gradient_boosting_regression_model import get_multimodal_model_1__gradient_boosting__calculate_air_quality__POWAC_ND
from mm_algorithms.mm_model_1.models.prediction.decision_tree_regression_model.decision_tree_regression_model import get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC_ND
from mm_algorithms.mm_model_1.models.prediction.random_forest_regression_model.random_forest_regression_model import get_multimodal_model_1__random_forest__calculate_air_quality__POWAC_ND


def weighting_nd(weights=(0.3, 0.5, 0.2)):
    # Ensure weights sum to 1
    assert len(weights) == 3, "Weights should be a list of three values."
    assert sum(weights) == 1, "Weights must sum to 1."

    # Get predictions from each model
    prediction_1 = get_multimodal_model_1__gradient_boosting__calculate_air_quality__POWAC_ND()
    prediction_2 = get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC_ND()
    prediction_3 = get_multimodal_model_1__random_forest__calculate_air_quality__POWAC_ND()

    # Weighted sum of predictions
    weighted_prediction = (weights[0] * prediction_1) + (weights[1] * prediction_2) + (weights[2] * prediction_3)

    return weighted_prediction
