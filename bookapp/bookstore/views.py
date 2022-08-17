import email
from multiprocessing import context
from re import U
from secrets import choice
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import User, Book, Chat, DeleteRequest, Feedback
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView, CreateView
from .forms import ChatForm, BookForm, UserForm, EmailForm, ProfileUpdateForm
from . import models
import operator
import itertools
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.



# Shared Views
def home(request):
    return render(request, 'student/index.html')

class EmailForm(CreateView):
    form_class = EmailForm
    model = User
    template_name = 'student/index.html'
    success_url = 'regform'
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


def login_form(request):
    return render(request, 'bookstore/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('/admin')
            else:
                return redirect('home')
        else:
            messages.info(request, "Invalid Username or password")
            return redirect('home')


def register_form(request):
    return render(request, 'student/register.html')

def registerView(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            password = make_password(password)

            a = User(username = username, email = email, password=password, first_name=first_name, last_name=last_name)
            a.save()
            messages.success(request, "Account was created successfully")
            return redirect('login_form')
        else:
            messages.error(request, 'Password not matching')
            return redirect('regform')
    else:
        messages.error(request, 'Registration Fail, try again later')
        return redirect('regform')

# student views

def student(request):
    return render(request, 'student/home.html')



@login_required
def request_form(request):
    return render(request, 'student/book_request.html')

@login_required
def feedback_form(request):
    return render(request, 'student/send_feedback.html')

@login_required
def about(request):
    return render(request, 'student/about.html')


def usearch(request):
    query = request.GET['query']
    print(type(query))
    
    
    data = query
    print(len(data))
    if(len(data) == 0):
        return redirect('student')
    else:
        a = data
        # title
        qs1 = models.Book.objects.filter(title__iexact=a).distinct()
        qs2 = models.Book.objects.all().filter(title__contains = a)
        qs3 = models.Book.objects.select_related().filter(title__contains=a).distinct()
        qs4 = models.Book.objects.filter(title__startswith=a).distinct()
        qs5 = models.Book.objects.filter(title__endswith=a).distinct()
        qs6 = models.Book.objects.filter(title__istartswith=a).distinct()
        qs7 = models.Book.objects.all().filter(title__icontains=a)
        qs8 = models.Book.objects.filter(title__iendswith=a).distinct()
        
        # id
        qs9 = models.Book.objects.filter(id__iexact=a).distinct()
        qs10 = models.Book.objects.all().filter(id__contains = a)
        qs11 = models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs12 = models.Book.objects.filter(id__startswith=a).distinct()
        qs13 = models.Book.objects.filter(id__endswith=a).distinct()
        qs14 = models.Book.objects.filter(id__istartswith=a).distinct()
        qs15 = models.Book.objects.all().filter(id__icontains=a)
        qs16 = models.Book.objects.filter(id__iendswith=a).distinct()
        
        # year
        qs17 = models.Book.objects.filter(year__iexact=a).distinct()
        qs18 = models.Book.objects.all().filter(year__contains = a)
        qs19 = models.Book.objects.select_related().filter(year__contains=a).distinct()
        qs20 = models.Book.objects.filter(year__startswith=a).distinct()
        qs21 = models.Book.objects.filter(year__endswith=a).distinct()
        qs22 = models.Book.objects.filter(year__istartswith=a).distinct()
        qs23 = models.Book.objects.all().filter(year__icontains=a)
        qs24 = models.Book.objects.filter(year__iendswith=a).distinct()
        
        files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13, qs14, qs15, qs16, qs17, qs18, qs19, qs20, qs21, qs22, qs23, qs24)
        res = []
        for i in files:
            if i not in res:
                res.append(i)
        
        word = "Searched Result :"
        print("Result")
        
        print(res)
        files = res
        
        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)
        
        if files:
            return render(request, 'student/result.html',{'files':files, 'word':word})
        return render(request, 'student/result.html', {'files':files, 'word':word})


@login_required
def book_request(request):
        if request.method == 'POST':
                book_id = request.POST['delete_request']
                current_user = request.user
                user_id = request.user
                user_id = current_user.id
                username = current_user.username
                user_request = username + "want book with id  " + book_id + "to be deleted"

                a = DeleteRequest(delete_request=user_request)
                a.save()
                messages.success(request, 'Request was sent')
                return redirect('request_form')
        else:
            messages.error(request, 'Request was not sent')
            return redirect('request_form')




@login_required
def send_feedback(request):
        if request.method == 'POST':
                feedback = request.POST['feedback']
                current_user = request.user
                user_id = request.user
                user_id = current_user.id
                username = current_user.username
                feedback = username + " " + "says" + feedback

                a = Feedback(feedback=feedback)
                a.save()
                messages.success(request, 'Request was sent')
                return redirect('feedback_form')
        else:
            messages.error(request, 'feedback was not sent')
            return redirect('feedback_form')


class UBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'student/book_list.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class UCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'student/chat_list.html'
    success_url = reverse_lazy('ulchat')

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'student/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('-posted_at')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'student/profile.html', context)