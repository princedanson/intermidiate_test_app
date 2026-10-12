from django.shortcuts import render
from django.http    import JsonResponse
from django.contrib.auth.decorators import login_required
import json,os
import requests,random,string
from .models import datasets

PORT = os.environ.get("PORT", "8000")
PREDICT_API = f"http://127.0.0.1:{PORT}/api/predict"
payload:dict = {str:str|int}


@login_required
def dashboard(request):
    request.session['savable'] = False
    result:str ="0"
    probability = 0
    global ERROR
    if request.method ==  "POST":

        if request.body:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                #print(body_data)
                payload = {
                    "Model_Type" : body_data.get("model"),
                    "Gender": body_data.get("gender"),
                    "Married": body_data.get("married"),
                    "Dependents": str(body_data.get("dependents")),
                    "Education": body_data.get("education"),
                    "Self_Employed": body_data.get("self_employed"),
                    "Property_Area": body_data.get("property area"),
                    "ApplicantIncome": body_data.get("ApplicantIncome",0),
                    "CoapplicantIncome": body_data.get("CoapplicantIncome",0),
                    "LoanAmount": body_data.get("LoanAmount",0),
                    "Loan_Amount_Term": body_data.get("Loan_Amount_Term",360),
                    "Credit_History": body_data.get("Credit_History",1)
                }

                try:
                    res = requests.post(PREDICT_API,json=payload,timeout=10)

                    res.raise_for_status() 
                    request.session['savable'] = True
                    payload.update({"Loan_ID": request.user.email})
                 
                except requests.RequestException as e:
                    request.session['savable'] = False
                    print("FASTAPI ERROR:",repr(e))
                    if e.response is not None:
                        print(e.response.status_code, e.response.text)
                        status_code = e.response.status_code
                        if status_code == 422:
                            try:
                                error_deatails = e.response.json()
                                print("Validation Error")
                                return JsonResponse({"error":"Validation Error",'details':error_deatails}, status= 422)
                            except json.JSONDecodeError:
                               print("Invalide input sent to the model")
                               return JsonResponse({"error":"Invalide input sent to the model"}, status=422)
                        print(f"Model server error status:{status_code}")
                        return JsonResponse({"error": f"Model server error status:{status_code}"}, status = status_code)
                    else:
                        print("Could not reach prediction server")
                        return JsonResponse({"error": "Could not reach prediction server"}, status = 500)
                print(res.json())
                payload.update(res.json())
                request.session['model_info'] = payload
                return JsonResponse(res.json(),safe=False)
            except json.JSONDecodeError:
                print (request.body.decode('utf-8',error='ignore'))
        else:
            print("Body is Empty")
        
        request.session['savable'] = False
        return JsonResponse({"title": "Dashboard",
                           "result":result,
                           "probability":probability})
     
    return render(request,"dashboard/dashboard.html",
                  {"title": "Dashboard"})

def save_data(request):
    
    if request.method == 'POST':
        if request.body :
            body_data = json.loads(request.body.decode('utf-8'))
            print(body_data)
            if not request.session.get("savable",False):
                print("Nothing to save!")
                return JsonResponse({"error":"Can't save data"}, status= 422)
                
            if body_data :
                print(request.session.get('model_info'))
                data = request.session.get('model_info',{})
                data.pop('selected')
                try:
                    save_to_dataset = datasets.objects.create(user= random.choice(string.ascii_letter + string.digits)+(request.user),**data)
                    save_to_dataset.save()
                    print(f"Successfully saved record ID {save_to_dataset.user} to database")
                    request.session['savable'] = False
                    
                    if 'model_info' in request.session:
                        del request.session['model_info']
                    return JsonResponse({"status":"SUCCESS","message":"Data Saved!"}, status = 200)
                except Exception as database_error:
                    print("Database save Failure",str(database_error))
                    return JsonResponse({'error':"Cant Save Entries!",'satus':"failed"})
            
    return render(request,"Dashboard/dashboard.html",{
        "Save":"saved",
    })
