from django.db import models
from django.contrib.auth.models import User 


class Disease(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserPredictions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    probablity = models.FloatField()
    symptom1 = models.CharField(max_length=100)
    symptom2 = models.CharField(max_length=100)
    symptom3 = models.CharField(max_length=100)
    symptom4 = models.CharField(max_length=100)
    symptom5 = models.CharField(max_length=100)
    symptom6 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.disease} - @{self.user} - {self.probablity}%"
    