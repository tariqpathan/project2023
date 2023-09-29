import pandas as pd
import numpy as np

from machine_learning.preprocess import main as preprocess_main


def dict2csv(filename: str):
    data = preprocess_main()
    df = pd.DataFrame(data)
    df['label'] = [None for _ in range(len(df))]
    df.to_csv(f'./ml_resources/{filename}.csv', index=False)


def csv2dict(filename: str):
    df = pd.read_csv(f'./ml_resources/{filename}.csv')
    data = df.to_dict('records')
    return data


def dict2csv_mod(filename: str):
    data = preprocess_main()  # Assuming this returns a list of dictionaries
    # Create a DataFrame from the data, but omit vectorized_text
    df_data = [{key: val for key, val in entry.items() if key != "vectorized_text"} for entry in data]
    df = pd.DataFrame(df_data)
    # Add a label column with None values
    df['label'] = [None for _ in range(len(df))]
    # Save the DataFrame to a CSV
    df.to_csv(f'./ml_resources/{filename}.csv', index=False)
    # Save just the vectorized_texts and their associated IDs to a separate file
    vector_data = [{"question_id": entry["question_id"], "vectorized_text": entry["vectorized_text"]} for entry in data]
    np.save(f'./ml_resources/{filename}_arrays.npy', vector_data)


def csv2dict_mod(filename: str):
    # Load the DataFrame from CSV
    df = pd.read_csv(f'./ml_resources/{filename}.csv')

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict('records')

    # Load the vectorized_texts and their associated IDs
    vector_data = np.load(f'./ml_resources/{filename}_arrays.npy', allow_pickle=True)

    vector_dict = {entry["question_id"]: entry["vectorized_text"] for entry in vector_data}

    # Merge vectorized_text back into data
    for entry in data:
        entry["vectorized_text"] = vector_dict.get(entry["question_id"])

    return data
