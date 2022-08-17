from signal import default_int_handler
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
# Create your models here.
class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    pdf = models.FileField(upload_to='bookapp/pdfs/')
    cover = models.ImageField(default='bookapp/covers/book.svg',upload_to='bookapp/covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        cover = Image.open(self.cover.path)
        
        if cover.height > 300 or cover.width > 300:
            output_size = (300, 300)
            cover.thumbnail(output_size)
            cover.save(self.cover.path)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.user)


class BookRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.title)

class DeleteRequest(models.Model):
    delete_request = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.delete_request

class Feedback(models.Model):
    feedback = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.feedback


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to ='profile_pics')
    
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    

class Testimony(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile,  on_delete=models.CASCADE)
    testimony = models.TextField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})