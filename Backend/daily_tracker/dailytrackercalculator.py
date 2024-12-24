import numpy as np
from sklearn.linear_model import LinearRegression

from backend.custom.customclasses import correlationStats

def calculate_data(data_x: list, data_y: list, name_x: str , name_y: str) -> correlationStats:
    data_x = np.array(data_x)
    data_y = np.array(data_y)
    mean_x = np.mean(data_x)
    mean_y = np.mean(data_y)
    numerator = np.sum((data_x - mean_x) * (data_y - mean_y))
    denominator = np.sqrt(np.sum((data_x - mean_x)**2) * np.sum((data_y - mean_y)**2))
    pmcc = numerator / denominator
    model = LinearRegression()
    model.fit(data_x, data_y)
    coef = model.coef_[0]
    stats = correlationStats(name_x, name_y, pmcc, coef) 
    return stats

