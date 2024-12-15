import pickle
import numpy as np
import os

def load_model(model_name: str = "logistic_regression_model", weights_dir: str ="weights"):
    """
    Load a pre-trained model from the weights directory.

    Args:
        model_name (str): The name of the model (without .pkl extension).
        weights_dir (str): The directory containing the saved model weights.

    Returns:
        model: The loaded model.
    
    Raises:
        FileNotFoundError: If the model file does not exist.
    """
    model_file = os.path.join(weights_dir, f"{model_name}.pkl")
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model '{model_file}' not found. Ensure the name is correct and the model is saved.")

    with open(model_file, "rb") as f:
        model = pickle.load(f)
    print(f"Model loaded successfully from {model_file}")
    return model

def predict_email(model, preprocessed_email):
    """
    Predict whether a given email is spam or not.

    Args:
        model: The loaded machine learning model.
        preprocessed_email (list or np.ndarray): The preprocessed email content represented as a feature vector.

    Returns:
        str: "spam" if the email is classified as spam, otherwise "not spam".
    """
    # Convert the preprocessed email into the format expected by the model
    email_vector = np.array(preprocessed_email).reshape(1, -1)

    # Make prediction
    prediction = model.predict(email_vector)[0]  # Get the first prediction

    # Interpret prediction
    return "spam" if prediction == 1 else "not spam"
