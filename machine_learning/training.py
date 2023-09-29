from typing import List

import joblib
import numpy as np
import ast

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

from machine_learning.dict_to_csv import csv2dict


def get_data(filename: str):
    data = csv2dict(filename)
    str_vectorized_texts = [entry["vectorized_text"] for entry in data]
    vector_array = convert_to_array(str_vectorized_texts)
    labels = [entry["label"] for entry in data]
    return vector_array, labels


def convert_to_array(vectorized_texts: List[str]) -> np.ndarray:
    """ Converts a list of string representations of arrays to a 2D numpy array.

    :param vectorized_texts:
    :return: a 2D numpy array

    """
    all_arrays = []
    # Loop through each string representation in vectorized_texts
    for string_representation in vectorized_texts:
        cleaned_str = string_representation.replace('[', '').replace(']', '').replace('\n', '')
        # Convert string to array using numpy.fromstring
        array = np.fromstring(cleaned_str, sep=' ')
        # Append the array to the list
        all_arrays.append(array)
    return np.vstack(all_arrays)


def main(filename: str):
    vectorized_texts, labels = get_data(filename)
    X_train, X_test, y_train, y_test = train_test_split(vectorized_texts, labels, test_size=0.2)

    classifier = MultinomialNB()
    classifier.fit(np.array(X_train), y_train)

    y_pred = classifier.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))

    joblib.dump(classifier, 'ml_resources/bio-classifier-1.joblib')

def predict():
    vectorizer = joblib.load('ml_resources/vectorizer.joblib')
    classifier = joblib.load('ml_resources/bio-classifier-1.joblib')
    text = 'engine car'
    vectorized_text = vectorizer.transform([text]).toarray()
    prediction = classifier.predict(vectorized_text)
    print(prediction)


if __name__ == "__main__":
    # main('bio-training')
    predict()