from django.shortcuts import render,redirect
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method != "POST":
        data={}
    else :
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        #すでにユーザーネームが使用されている
        if(User.objects.filter(username=username).exists()):
            print(1)
            data = {"message":"すでに存在するユーザーネームです"}
        #パスワードが一致しない場合
        elif(password != repassword):
            data = {"message":"パスワードが一致しません","username":username}
        #ユーザーの作成に成功
        else:
            newuser = User.objects.create_user(username = username)
            newuser.set_password(password)
            newuser.save()
            return redirect("login")

    return render(request,'accounts/signup.html',data)