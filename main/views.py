from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from main.models import TimeTable,LessonField,Separation
from main.timetable import createtimetable
from django.utils import timezone
import copy
from . import color
from django.utils.timezone import localtime 
# Create your views here.

@login_required
def home(request):
    user = request.user
    if(not TimeTable.objects.filter(user = user).exists()):
        return render(request,"main/home.html")
    now = localtime(timezone.now())
    text=["月","火","水","木","金","土","日"]
    timetable = TimeTable.objects.get(user = user)
    separations = Separation.objects.filter(timetable=timetable).order_by("period")
    contents = []
    t = now.strftime('%H:%M')
    print(t)
    i = now.weekday()
    for sep in separations:
        print(sep.get_already(t))
        if(sep.get_already(t)!=True and LessonField.objects.filter(period=sep.period,dayof=i,timetable=timetable).exists()):
            lesson = LessonField.objects.get(period=sep.period,dayof=i,timetable=timetable)
            print(sep.end)
            d={"lesson":lesson,"sep":sep}
            contents.append(d)
    data={"contents":contents}
    print(data)
    return render(request,"main/home.html",data)

@login_required
def timetable(request):
    user = request.user
    if(not TimeTable.objects.filter(user = user).exists()):
        return redirect("main:tablestatus")
    timetable = TimeTable.objects.get(user = user)
    separations = Separation.objects.filter(timetable=timetable).order_by("period")
    contents = []
    for sep in separations:
        ds=[]
        for i in range(6):
            if(LessonField.objects.filter(period=sep.period,dayof=i,timetable=timetable).exists()):
                lesson = LessonField.objects.get(period=sep.period,dayof=i,timetable=timetable)
                print(lesson.name+":"+str(lesson.period)+":"+str(lesson.dayof))
                d={"name":lesson.name,"color":lesson.color,"id":lesson.id}
                ds.append(d)
            else:
                ds.append({"name":""})
        data = {"period" : sep,"week":ds}
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
    if(LessonField.objects.filter(period = int(request.POST['periodnum']),dayof = int(request.POST['dayof']),timetable=timetable).exists()):
        data={"nums":range(1,separations.count()+1),"alert":"そのスペースにはすでに授業が存在します"}
        return render(request,"timetable/createlessonfield.html",data)
    lesson = LessonField.objects.create(
    name = request.POST["name"],
    color = request.POST['color'],
    period = int(request.POST['periodnum']),
    dayof = int(request.POST['dayof']),
    content = request.POST['content'],
    timetable = timetable)
    lesson.save()
    return redirect("main:home")

@login_required
def contentslessonfield(request,id):
    user = request.user
    if(not TimeTable.objects.filter(user = user).exists()):
        return redirect("main:tablestatus")

    timetable=TimeTable.objects.get(user = user)
    separations = Separation.objects.filter(timetable=timetable).order_by("period")

    if(not LessonField.objects.filter(id=id,timetable=timetable).exists()):
        return redirect("main:home")

    lesson=LessonField.objects.get(id=id)

    if(request.method == "POST"):
        if(request.POST["request"]=="changepage"):
            colors = color.Colors()
            colorlst=colors.get_color()
            c=[]
            for i in range(colors.get_len()):
                data={"color":colorlst[i],"selected":colorlst[i]==lesson.color}
                c.append(data)
            data={"nums":range(1,separations.count()+1),"lesson":lesson,"type":"changecontent","colors":c}
            return render(request,"timetable/contentslessonfield.html",data)
        if(request.POST["request"]=="changecontents"):
            lesson.name=request.POST["name"]
            lesson.content=request.POST["content"]
            lesson.color=request.POST["color"]
            lesson.save()
        if(request.POST["request"]=="deletepage"):
            lesson.delete()
            return redirect("main:timetable")
    text=["月","火","水","木","金","土"]
    data={"lesson":lesson,"week":text[lesson.dayof],"type":"nomal"}
    return render(request,"timetable/contentslessonfield.html",data)



    
    
    
    