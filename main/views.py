from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from main.models import TimeTable,LessonField,link,Separation
from main.timetable import createtimetable
# Create your views here.

@login_required
def home(request):
    return render(request,"main/home.html")

@login_required
def timetable(request):
    user = request.user
    if(not TimeTable.objects.filter(user = user).exists()):
        return redirect("main:tablestatus")
    timetable = TimeTable.objects.get(user = user)
    separations = Separation.objects.filter(timetable=timetable).order_by("period")
    contents = []
    for sep in separations:
        d={"name":""}
        ds=[d,d,d,d,d,d]
        data = {"period" : sep,"mon":ds[0],"tue":ds[1],"wed":ds[2],"thu":ds[3],"fri":ds[4],"sta":ds[5]}
        contents.append(data)
    data={"contents":contents}
    return render(request,"timetable/main.html",data)

@login_required
def tablestatus(request):
    message=None
    seps=[]
    user = request.user
    try: 
        if(not TimeTable.objects.filter(user = user).exists()):
            timetable = createtimetable(user)
        else:
            timetable=TimeTable.objects.get(user = user)
    except:
        timetable = createtimetable(user)
    if(request.method=="POST"):
        print(0)
        if(request.POST["type"]=="add"):
            new = Separation.objects.create(timetable=timetable,start="00:00",end="00:00",period=Separation.objects.filter(timetable=timetable).count()+1)
            print(1)
        elif(request.POST["type"]=="del"):
            separations = Separation.objects.filter(timetable=timetable).order_by("period")
            separations[separations.count()-1].delete()
            print(2)
        else:
            strs=[]
            change=True
            for i in ["starth","startm","endh","endm"]:
                s = request.POST[i]
                print(s)
                if(not(len(s)>0 and len(s)<3)):
                    message = "入力が正しくありません"
                    change=False
                    break
                elif(not(s.isdecimal())):
                    message = "入力が正しくありません"
                    change=False
                    break
                else:
                    strs.append(s)
            if(change):
                start = strs[0]+":"+strs[1]
                end = strs[2]+":"+strs[3]
                sep = Separation.objects.get(timetable=timetable,period=int(request.POST["num"]))
                sep.start = start
                sep.end = end
                sep.save()
                print(3)

    separations = Separation.objects.filter(timetable=timetable).order_by("period")
    for sep in separations:
        starth,startm = sep.get_start()
        endh,endm = sep.get_end()
        content = {"starth":str(starth).zfill(2),"startm":str(startm).zfill(2),"endh":str(endh).zfill(2),"endm":str(endm).zfill(2),"period":sep.period}
        seps.append(content)
    data = {"timetable":timetable,"seps":seps,"message":message}
    return render(request,"timetable/tablestatus.html",data)

@login_required
def createlessonfield(request):
    user = request.user
    if(not TimeTable.objects.filter(user = user).exists()):
        return redirect("main:tablestatus")
    timetable=TimeTable.objects.get(user = user)
    separations = Separation.objects.filter(timetable=timetable).order_by("period")
    if(request.method!="POST"):
        data={"nums":range(1,separations.count()+1)}
        return render(request,"timetable/createlessonfield.html",data)
    
    
    