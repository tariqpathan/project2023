import re
import nltk
import numpy as np
import pytesseract

from typing import Dict, List
from sqlalchemy.orm import Session
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from database.models import Question
from database.database_manager import DatabaseManager
from extraction_engine.managers.file_manager import FileManager
from extraction_engine.managers.image_file_handler import ImageFileHandler

nltk.download('stopwords')
nltk.download('wordnet')


def get_questions(session: Session) -> List[Question]:
    return session.query(Question).all()


def ocr_image(image_filename: str) -> str:
    img = ImageFileHandler.get_image(image_filename)
    return pytesseract.image_to_string(img).lower()


def preprocess_text(text: str) -> str:
    # Convert text to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


def remove_stopwords(text: str) -> str:
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)


def length_filter(text: str) -> str:
    words = text.split()
    words = [word for word in words if 3 < len(word) < 15]
    return ' '.join(words)


def lemmatize_text(text: str) -> str:
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)


def vectorize_texts(texts: List[str]) -> np.ndarray:
    vectorizer = TfidfVectorizer()
    vectorizer.fit(texts)  # fit() expects a list of documents
    return vectorizer.transform(texts).toarray()


def pipeline(db_manager: DatabaseManager) -> List[Dict]:
    with db_manager.get_session() as session:
        questions = get_questions(session)

        processed_data = []

        texts_to_vectorize = []

        for question in questions:
            raw_text = ocr_image(question.image_filename)
            preprocessed_text = preprocess_text(raw_text)
            filtered_text = length_filter(preprocessed_text)
            text_wo_stopwords = remove_stopwords(filtered_text)
            lemmatized_text = lemmatize_text(text_wo_stopwords)

            processed_entry = {
                "question_id": question.id,  # do i need this?
                "raw_text": raw_text,
                "lemmatized_text": lemmatized_text
            }
            processed_data.append(processed_entry)

            texts_to_vectorize.append(lemmatized_text)

        # vectorize the texts that were collected and add them to the processed_data
        vectorized = vectorize_texts(texts_to_vectorize)
        for i, data in enumerate(processed_data):
            data["vectorized_text"] = vectorized[i]

    return processed_data


# def add_labels(processed_data: List[Dict]) -> List[Dict]:
#     for p in processed_data:
#         p["label"] = None
#     return processed_data


def main():
    db_path = FileManager.get_filepaths("db_path").as_posix()
    db_manager = DatabaseManager(db_path)

    processed_data = pipeline(db_manager)

    return processed_data

if __name__ == '__main__':
    main()
