import numpy as np

def detect_anomalies(data, threshold=2.5):
    """
    Detects anomalies in a list of numbers using the Z-score method.
    Returns a list of indices where anomalies are found.
    """
    if not data or len(data) < 2:
        return []
    
    mean = np.mean(data)
    std = np.std(data)
    
    if std == 0:
        return []

    anomalies = []
    for i, x in enumerate(data):
        z_score = (x - mean) / std
        if abs(z_score) > threshold:
            anomalies.append(i)
            
    return anomalies