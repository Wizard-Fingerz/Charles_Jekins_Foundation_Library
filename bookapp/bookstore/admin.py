from django.contrib import admin
from .models import BookRequest, User, Book, Chat, DeleteRequest, Feedback

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff','is_student')
    search_fields = ['username', 'first_name', 'last_name', 'is_student']


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'publisher','desc', 'uploaded_by')
    list_filter = ('year', 'publisher','uploaded_by')
    search_fields = ['title', 'author', 'year', 'publisher','desc', 'uploaded_by']
    list_editable = ['author', 'publisher']

class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'year', 'publisher','desc')
    list_filter = ('year', 'publisher')
    search_fields = ['title', 'author', 'year', 'publisher','desc']
    list_editable = ['author', 'year', 'publisher']
    
    
admin.site.site_header = "Charles Jekins Library Administration"
admin.site.register([Chat, DeleteRequest, Feedback])
admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookRequest, BookRequestAdmin)