from django.contrib.auth.models import User
from main.models import TimeTable,LessonField,Separation

start = ["9:00","10:40","13:00","14:45","16:30"]
end = ["10:30","12:10","14:30","16:15","18:00"] 
def createtimetable(user):
    timetable = TimeTable.objects.create(name = "時間割",user = user)
    for i in range(5):
        Separation.objects.create(period = i+1,start=start[i],end=end[i],timetable=timetable)
    return timetable

