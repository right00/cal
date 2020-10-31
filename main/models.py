from django.db import models
from django.conf import settings
from django.utils import timezone
import re

# Create your models here.

class TimeTable(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class LessonField(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=30,default="white")
    period = models.IntegerField()
    dayof = models.IntegerField()
    content = models.TextField()
    timetable = models.ForeignKey(TimeTable,on_delete=models.CASCADE)


class Separation(models.Model):
    period = models.IntegerField()
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    timetable = models.ForeignKey(TimeTable,on_delete=models.CASCADE)
    
    def get_start(self):
        num = re.match(r'([0-9]{1,2}):([0-9]{1,2})', self.start)
        result = num.groups()
        return  int(result[0]),int(result[1])

    def get_end(self):
        num = re.match(r'([0-9]{1,2}):([0-9]{1,2})', self.end)
        result = num.groups()
        return  int(result[0]),int(result[1])
        
    def get_already(self,now):
        num = re.match(r'([0-9]{1,2}):([0-9]{1,2})', self.end) 
        result = num.groups()
        now = re.match(r'([0-9]{1,2}):([0-9]{1,2})', now)
        result_now = now.groups()
        
        if(int(result[0])<int(result_now[0])):
            return True
        
        elif(int(result[0])==int(result_now[0]) and int(result[1])<int(result_now[1])):
            return True 
        
        return False
    
