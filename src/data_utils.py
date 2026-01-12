"""
Data loading and preprocessing utilities
"""

import json
from pathlib import Path
from typing import List, Tuple

def load_json_data(filepath: Path) -> List[dict]:
    """Load JSON data from file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_features_and_labels(data: List[dict]) -> Tuple[List[List[float]], List[int]]:
    """
    Extract features and labels from iris data
    
    Returns:
        X: List of feature vectors (4 features each)
        y: List of class labels (0, 1, 2)
    """
    species_map = {"setosa": 0, "versicolor": 1, "virginica": 2}
    
    X = []
    y = []
    
    for sample in data:
        features = [
            sample["sepal_length"],
            sample["sepal_width"],
            sample["petal_length"],
            sample["petal_width"]
        ]
        X.append(features)
        
        # Use class_name field if available, otherwise class field
        if "class_name" in sample:
            label = species_map[sample["class_name"]]
        else:
            label = sample["class"]
        y.append(label)
    
    return X, y

def prepare_dataset(filepath: Path) -> Tuple[List[List[float]], List[int]]:
    """Load and prepare dataset in one step"""
    data = load_json_data(filepath)
    return extract_features_and_labels(data)
