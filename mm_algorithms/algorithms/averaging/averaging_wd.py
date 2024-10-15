from mm_algorithms.mm_model_1.models.prediction.gradient_boosting_regression_model.gradient_boosting_regression_model import get_multimodal_model_1__gradient_boosting__calculate_air_quality__POWAC
from mm_algorithms.mm_model_1.models.prediction.decision_tree_regression_model.decision_tree_regression_model import get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC
from mm_algorithms.mm_model_1.models.prediction.random_forest_regression_model.random_forest_regression_model import get_multimodal_model_1__random_forest__calculate_air_quality__POWAC


def averaging_wd():
    prediction_1 = get_multimodal_model_1__gradient_boosting__calculate_air_quality__POWAC()
    prediction_2 = get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC()
    prediction_3 = get_multimodal_model_1__random_forest__calculate_air_quality__POWAC()

    print("Prediction 1: ", prediction_1)
    print("Prediction 2: ", prediction_2)
    print("Prediction 3: ", prediction_3)

    return (prediction_1 + prediction_2 + prediction_3) / 3



