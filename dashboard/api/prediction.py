import sys
from dashboard.ml import loan_preprocessing
sys.modules['loan_preprocessing'] = loan_preprocessing
from fastapi import FastAPI
from fastapi_offline import FastAPIOffline
from pydantic import BaseModel

import pandas as pd

from dashboard.ml.service import predict


predict_api = FastAPI()
#predict_api = FastAPIOffline()
class PredictionInput(BaseModel):
    #Model type
    Model_Type:str

    #features
    Gender:str
    Married:str
    Dependents:str
    Education:str
    Self_Employed:str
    Property_Area:str
    ApplicantIncome:int
    CoapplicantIncome:int
    LoanAmount:int
    Loan_Amount_Term:int
    Credit_History:int


    

@predict_api.post("/predict")
def predict_loan(data:PredictionInput):
    input = data.model_dump()
    model_type = input.pop("Model_Type")
    
    df = pd.DataFrame([input])
    result = predict(df,model_type)
    return result

