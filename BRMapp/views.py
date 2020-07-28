from django.shortcuts import render
from BRMapp.forms import NewBookForm,SearchForm
from BRMapp import models
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def userLogin(request):
    data={}
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            request.session['username']=username

            return HttpResponseRedirect('/BRMapp/view-books')
        else:
            data['error']="username or password is incorrect"
            res=render(request,'BRMapp/user_login.html',data)
            return res
    else:
        res=render(request,'BRMapp/user_login.html',data)
        return res
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/BRMapp/login/')

@login_required(login_url='/BRMapp/login/')
def viewBooks(request):
    books=models.Book.objects.all()
    username=request.session['username']
    res=render(request,'BRMapp/view_book.html',{'books':books,'username':username})
    return res
@login_required(login_url='/BRMapp/login/')
def deleteBook(request):
    bookid=request.GET['bookid']
    book=models.Book.objects.filter(id=bookid)
    book.delete()
    return HttpResponseRedirect('BRMapp/view-books')
@login_required(login_url='/BRMapp/login/')
def search(request):
    form=SearchForm(request.POST)
    books=models.Book.objects.filter(title=form.data['title'])
    res=render(request,'BRMapp/search_book.html',{'form':form,'books':books})
    return res
@login_required(login_url='/BRMapp/login/')
def searchBook(request):
    form=SearchForm()
    res=render(request,'BRMapp/search_book.html',{'form':form})
    return res
@login_required(login_url='/BRMapp/login/')
def editBook(request):
    book=models.Book.objects.get(id=request.GET['bookid'])
    fields={'title':book.title,'price':book.price,'author':book.author,'publisher':book.publisher}
    form=NewBookForm(initial=fields)
    res=render(request,'BRMapp/edit_book.html',{'form':form,'book':book})
    return res

@login_required(login_url='/BRMapp/login/')
def edit(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book= models.Book()
        bookid =request.POST['bookid']
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()

    return HttpResponseRedirect('BRMapp/view-books')
@login_required(login_url='/BRMapp/login/')
def newBook(request):
    form=NewBookForm()
    res=render(request,'BRMapp/new_book.html',{'form':form})
    return res
@login_required(login_url='/BRMapp/login/')
def add(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    s="Record Savd <br> <a href='/BRMapp/view-books'>view all books </a>"
    return HttpResponse(s)
