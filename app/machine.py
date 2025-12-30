from datetime import datetime
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


class Machine:
    def __init__(self, df: DataFrame):
        self.name = "Random Forest Classifier"
        self.created_at = datetime.utcnow()

        # 🎯 Target (what we predict)
        target = df["Rarity"]

        # 🎯 Features (what we learn from)
        features = df[["Level", "Health", "Energy", "Sanity"]]

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", "passthrough", ["Level", "Health", "Energy", "Sanity"]),
            ]
        )

        self.model = Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("classifier", RandomForestClassifier(random_state=42)),
            ]
        )

        self.model.fit(features, target)

    def __call__(self, pred_basis: DataFrame):
        prediction = self.model.predict(pred_basis)[0]
        probability = max(self.model.predict_proba(pred_basis)[0])
        return prediction, probability

    def save(self, filepath: str):
        joblib.dump(self, filepath)

    @classmethod
    def open(cls, filepath: str):
        return joblib.load(filepath)

    def info(self) -> str:
        return f"{self.name} | initialized at {self.created_at.isoformat()}"
