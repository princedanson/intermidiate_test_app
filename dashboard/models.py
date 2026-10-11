from django.db import models
from django.contrib.auth.models import User
class datasets(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='predictions')
    Loan_ID = models.EmailField(max_length=50,unique=True)
    Model_Type = models.CharField()
    Gender = models.CharField()
    Married = models.CharField()
    Dependents = models.CharField()
    Education = models.CharField()
    Self_Employed = models.CharField()
    Property_Area = models.CharField()
    ApplicantIncome = models.BigIntegerField()
    CoapplicantIncome = models.BigIntegerField()
    LoanAmount = models.BigIntegerField()
    Loan_Amount_Term = models.BigIntegerField()
    Credit_History = models.BigIntegerField()
    
    result = models.CharField(max_length=50,blank=True,null=True)
    probability = models.FloatField(blank=True,null=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Loan_ID} "