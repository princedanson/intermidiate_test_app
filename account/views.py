from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
def logout(request):
    auth.logout(request)
    return  redirect("/account/login")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            next_Url = request.GET.get("next")
            return redirect(next_Url or "dashboard:dashboard")

        else:
            return render(request,"account/login.html",
                      {
                          "error": "Invalid User!"
                      })
    

    else:
        return render(request,"account/login.html",
                      {
                          "title": "Login"
                      })
def create_account(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "account/create.html",{
                            "error": "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request,"account/create.html",
                          {
                           "error":" User Name Taken!"})
        if User.objects.filter(email=email).exists():
            return render(request,"account/create.html",{
                          "error":"Email already exist!"})
        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        
        print("User Saved!")
        return redirect('account:login')
    else:
        return render(request, "account/create.html", {"title": "Create Account"})   
