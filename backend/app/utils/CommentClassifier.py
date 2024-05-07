import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk as nltk
import joblib as joblib
from typing import Tuple, List
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class CommentClassifier:
    def __init__(self):
        self.train_data_path = "combined_comments.csv"
        self.joblib_path = "trained_comment_classifier.joblib"
        self.random_state = 42
        self.rating_model = None
        self.toxicity_model = None

    def preprocess_text(self, text: str) -> str:
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha() and token.lower() not in stop_words]
        return ' '.join(tokens)

    def train(self) -> None:
        data = pd.read_csv(self.train_data_path)
        data['comment'] = data['comment'].apply(self.preprocess_text)
        x_train, x_val, y_rating_train, y_rating_val, y_toxicity_train, y_toxicity_val = \
            train_test_split(data['comment'], data['rating'], data['toxicity'], test_size=0.2, random_state=self.random_state)
        pipeline_rating = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=1000, random_state=self.random_state))
        ])
        pipeline_toxicity = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=1000, random_state=self.random_state))
        ])
        param_grid = {'clf__C': [0.1, 1, 10]}
        grid_search_rating = GridSearchCV(pipeline_rating, param_grid, cv=5)
        grid_search_toxicity = GridSearchCV(pipeline_toxicity, param_grid, cv=5)
        grid_search_rating.fit(x_train, y_rating_train)
        grid_search_toxicity.fit(x_train, y_toxicity_train)
        self.rating_model = grid_search_rating.best_estimator_
        self.toxicity_model = grid_search_toxicity.best_estimator_
        rating_train_predictions = self.rating_model.predict(x_val)
        toxicity_train_predictions = self.toxicity_model.predict(x_val)
        print("Rating Model Evaluation:")
        print(classification_report(y_rating_val, rating_train_predictions))
        print("Toxicity Model Evaluation:")
        print(classification_report(y_toxicity_val, toxicity_train_predictions))

    def predict(self, comment: str) -> Tuple[int, bool]:
        if self.rating_model is None or self.toxicity_model is None:
            raise ValueError("Models are not trained. Please train the models first.")
        preprocessed_comment = self.preprocess_text(comment)
        rating_prediction = int(self.rating_model.predict([preprocessed_comment])[0])
        toxicity_prediction = bool(self.toxicity_model.predict([preprocessed_comment])[0])
        return rating_prediction, toxicity_prediction

    def save(self) -> None:
        if self.rating_model is None or self.toxicity_model is None:
            raise ValueError("Models are not trained. Please train the models first.")
        joblib.dump((self.rating_model, self.toxicity_model), self.joblib_path)

    def load(self) -> None:
        self.rating_model, self.toxicity_model = joblib.load(self.joblib_path)

__all__ = [
    "CommentClassifier"
]