from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Pizaa(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to= 'Pizaa/')
    price=models.PositiveIntegerField()
    description=models.TextField()


    
    def __str__(self):
        return self.name


