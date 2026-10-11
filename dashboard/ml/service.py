import joblib
import pandas as pd
from pathlib import Path

test = pd.read_csv("dashboard/ml/loan_dataset/test_Y3wMUE5_7gLdaTN.csv")
ML_DIR = Path(__file__).resolve().parent / "models"
MODEL_FILES = {
                'Logistic Regression': "logistic_regression.joblib",
                "Decision Tree": "decision_tree_.joblib",
                "Random Forest": "random_forest.joblib",
                "Gradient Boosting": "gradient_boosting.joblib",
                "Bayes Multinominal": "bayes_multinominal.joblib",
                "XGBoost": "xgboost.joblib",
                "SVC": "svm.joblib",
                "KNN": "knn.joblib"
                }
MODEL = {model_name : joblib.load(ML_DIR/model)  for model_name , model in MODEL_FILES.items()}
def predict(data:pd.DataFrame,model_type:str)->dict:
        result = None
        probability =None
        selected:str =  model_type
        #print(MODEL)
        model = MODEL.get(selected)
        print(model)
        if model is None:
                result = "Please choose a model"
        else:
                print(f"this model was selected{selected}")
                pred = model.predict(data)[0]
                result = "Approved" if pred == 1 else "Rejected"
                if hasattr(model,"predict_proba"):
                        probability = round(model.predict_proba(data)[0][1]*100,1)
        render = {
                "result": str(result),
               "probability":round(float(probability),2),
                "selected": str(selected),
        }
        return render
y = predict(test,"XGBoost")
print(y)
