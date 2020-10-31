from django.shortcuts import render,redirect
from accounts.models import User

# Create your views here.
def signup(request):
    if request.method != "POST":
        data={}
    else :
        email = request.POST["email"]
        password = request.POST["pw"]
        repassword = request.POST["rpw"]
        #パスワードが一致しない場合
        if(password != repassword or len(password)<4 or password==None):
            data = {"message":"パスワードに誤りがあります","email":email}
        #ユーザーの作成に成功
        else:
            newuser = User.objects.create_user(email = email)
            newuser.set_password(password)
            newuser.save()
            return redirect("login")

    return render(request,'accounts/signup.html',data)