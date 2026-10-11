import kagglehub
import pandas as pd
from pathlib import Path
import os
import joblib
from sklearn.pipeline import Pipeline
from  loan_preprocessing import LoanPreprocessing

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.calibration import  CalibratedClassifierCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score,ConfusionMatrixDisplay)
                             
#path = kagglehub.dataset_download("altruistdelhite04/loan-prediction-problem-dataset")
#loan_ds = pd.read_csv(os.path.join(path, "train_u6lujuX_CVtuZ9i.csv"))

ML_DIR = Path(__file__).resolve().parent / "models"

loan_ds_train = pd.read_csv("dashboard/ml/loan_dataset/train_u6lujuX_CVtuZ9i.csv")
loan_ds_test = pd.read_csv("dashboard/ml/loan_dataset/test_Y3wMUE5_7gLdaTN.csv")

raw_x_train= loan_ds_train.drop(columns=["Loan_ID","Loan_Status"])
raw_y_train = loan_ds_train["Loan_Status"].map({"Y":1, "N": 0})

raw_x_test= loan_ds_test.drop(columns=["Loan_ID"])
#raw_y_test = loan_ds_test["Loan_Status"].map({"Y":1, "N": 0})

print("Heelo")
# x_train, x_test, y_train, y_test = train_test_split(raw_x,loan_y,test_size=0.2, random_state=42)

classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "Bayes Multinominal": GaussianNB(),
        "XGBoost": XGBClassifier(),
        "SVM": CalibratedClassifierCV(SVC(),ensemble = False),
        "KNN": KNeighborsClassifier()
}

pipelines, scores = {},{}
for name, clf in classifiers.items():
    pipe = Pipeline([("prep",LoanPreprocessing()),
                     ("model",clf)])
    pipe.fit(raw_x_train,raw_y_train)
    pred = pipe.predict(raw_x_test)
    #scores[name] = f1_score(raw_x_test,pred,average="macro")
    joblib.dump(pipe,ML_DIR/(f"{name.replace(' ','_').lower()}.joblib"))


