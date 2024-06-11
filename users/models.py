from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True,default='default_img/user.png')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    

