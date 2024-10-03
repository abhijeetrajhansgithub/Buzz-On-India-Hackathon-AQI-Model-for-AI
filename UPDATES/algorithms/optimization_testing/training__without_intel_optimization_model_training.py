def get_time__without_intel_optimization_model_training():
    # Import necessary libraries
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.svm import SVR
    from sklearn.neural_network import MLPRegressor
    import time

    # Load the dataset (replace 'your_dataset.csv' with the path to your actual dataset)
    data = pd.read_csv(r'../../data/preprocessed_data.csv')

    # Define the features and target variables
    X = data.drop(['pm2_5', 'pm10'], axis=1)  # Drop target columns
    y_pm2_5 = data['pm2_5']
    y_pm10 = data['pm10']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train_pm2_5, y_test_pm2_5 = train_test_split(X, y_pm2_5, test_size=0.2, random_state=42)
    _, _, y_train_pm10, y_test_pm10 = train_test_split(X, y_pm10, test_size=0.2, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Helper function to evaluate model performance
    def evaluate_model(model, X_test, y_test):
        y_pred = model.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)
        return rmse, r2

    # Initialize models
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree Regression': DecisionTreeRegressor(),
        'Random Forest Regression': RandomForestRegressor(n_estimators=100),
        'Support Vector Regression (SVR)': SVR(),
        'Neural Network Regression (MLP)': MLPRegressor(hidden_layer_sizes=(100,), max_iter=500),
        'Gradient Boosting Regression': GradientBoostingRegressor()
    }

    # Measure time for training and evaluation
    start_time = time.time()

    # Train and evaluate models for pm2_5
    for model_name, model in models.items():
        model.fit(X_train, y_train_pm2_5)
        rmse, r2 = evaluate_model(model, X_test, y_test_pm2_5)

    # Train and evaluate models for pm10
    for model_name, model in models.items():
        model.fit(X_train, y_train_pm10)
        rmse, r2 = evaluate_model(model, X_test, y_test_pm10)

    end_time = time.time()
    time_taken = end_time - start_time

    return {"Model training without Intel": time_taken}
