import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

LOG_COLS = ["ApplicantIncome","CoapplicantIncome","LoanAmount"]
MAPPING ={
            "Female": 0,
            "Male": 1,
            "Graduate": 1,
            "Not Graduate": 0,
            "Urban": 1,
            "Rural": 0,
            "Semiurban": 2,  # Added mapping for 'Semiurban'
            'Yes': 1,
            "No": 0,
            "N": 0,
            "Y": 1,
            "0": 0, "1": 1, "2": 2, "3+": 3
}

class LoanPreprocessing(BaseEstimator,TransformerMixin):

    def _encode(self,X):
        X = X.drop(columns=["Loan_ID","Loan_Status"], errors ="ignore")
        X = X.replace(MAPPING)
        return X.apply(pd.to_numeric,errors="coerce").astype(float)

    def _prepare(self,X):
        X = X.fillna(self.fill_)
        X[LOG_COLS] = np.log1p(X[LOG_COLS])
        return X

    def fit(self,  X,y=None):
        X = self._encode(X)
        self.features_= list(X.columns)
        self.fill_ = {c: (X[c].median() if c in LOG_COLS else X[c].mode()[0])
                      for c in X.columns}
        X = self._prepare(X)
        self.mean_ = X.mean()
        self.std_ = X.std()
        
        return self
    
    def transform(self,X):
        #print(X.head(3))
        X = self._encode(X)[self.features_]
        X = self._prepare(X)
        #print(X.head(2))
        return (X - self.mean_)/self.std_
    
def scaling(data,cols):
    # scaling using z-score
    loan_scaled = data[cols]
    for col in cols:
        loan_scaled[col] = (data[col] - data[col].mean()) / data[col].std()

    return loan_scaled

