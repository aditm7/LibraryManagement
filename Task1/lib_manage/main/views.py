from django.shortcuts import render,HttpResponse,redirect
from main.models import book,userinfo,booking
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from datetime import date,timedelta

def login_user(request):
  return render(request,'login.html')

def nominee(request):
  if request.method=="POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
      login(request,user)
      messages.success(request,"You are successfully logged in as ")
      t = userinfo.objects.get(username=username)
      if t.role=='student':
        variables ={
        "name":t.name,
        "hostel":t.hostel,
        "email":t.email,
        "username":t.username,
        "year":t.year,
        }
        return render(request,'base1.html',variables)
      else:
        t=userinfo.objects.get(username=request.user)
        return render(request,'librarian.html',{"t":t})
    else:
      return render(request,'login.html')
  elif request.user.is_anonymous:
    return render(request,'login.html')
  else:
    t = userinfo.objects.get(username=request.user)
    if t.role=='student':
      variables ={
      "name":t.name,
      "hostel":t.hostel,
      "email":t.email,
      "username":t.username,
      "year":t.year,
      }
      return render(request,'base1.html',variables)

def logout_user(request):
  logout(request)
  messages.success(request,"You have successfully logged out")
  return redirect("/")

def register_user(request):
  if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    year = request.POST.get('year')
    hostel = request.POST.get('hostel')
    info = userinfo(name=name,email=email,hostel=hostel,year=year,username=username)
    info.save()
    User.objects.create_user(username=username, password=password)
    messages.success(request,"User Registered successfully")
    return render(request,'register.html')
  
  else:
    return render(request,'register.html')

def book_main(request,n):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method =='POST':
    b = book.objects.get(code=n)
    a = b.available
    ko = "/"+str(n)
    current_user=request.user
    ls = userinfo.objects.get(username=current_user)
    if a=="yes":
      b.available="hold"
      bookin = booking(book=b,user=ls,idate=date.today(),edate=date.today() + timedelta(days=14),waiting_no=b.waiting_no)
      b.save()
      bookin.save()
      messages.success(request,"The book booked successfully, wait for approval")
      return redirect(ko)
    elif a=="hold":
      ls1 = booking.objects.filter(book__available__contains="no",user__username__contains=request.user)
      for i in ls1:
        if i.book.name==b.name and i.user.name==current_user:
          messages.warning(request,"You have already submitted a request for booking this book")
          return redirect(ko)
        messages.error(request,"Currently the book is on hold so can't be booked")
        return redirect(ko)
    elif a=="no":
      ls1 = booking.objects.filter(book__available__contains="no",user__username__contains=request.user)
      for i in ls1:
        if i.book.name==b.name and i.user.name==current_user:
          messages.warning(request,"You have already submitted a request for booking this book")
          return redirect(ko)
        else:
          messages.error(request,"You have already successfully borrowed this book")
          return redirect(ko)
      b.available="hold"
      bookin = booking(book=b,user=ls,idate=date.today(),edate=date.today() + timedelta(days=14))
      b.save()
      bookin.save()
      messages.success(request,"The book booked successfully, wait for approval")
      return redirect(ko)
  else:
    b = book.objects.get(code=n)
    var = {
      "name": b.name,
      "author": b.author,
      "publisher": b.publisher,
      "genre":b.genre,
      "summary":b.summary,
      "final_rating":b.final_rating,
      "isbn":b.isbn,
      "waiting_no":b.waiting_no,
      "rating_count":b.rating_count,
      "code":b.code,
    }
    a=b.available
    if a=="hold":
      var["color"] ="blue"
      var["available"]="In hold"
    elif a=="no":
      var["color"]= "red"
      var["available"]="waiting ("+str(b.waiting_no)+")"
    else:
      var["color"]= "green"
      var["available"]="Available to borrow"
    var["username"]=request.user
    return render(request,'bookmain.html',var)

def borrowed(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method == 'POST':
    if userinfo.objects.get(username=request.user).role=='student':
      current_user = request.user
      t = userinfo.objects.get(username=current_user)
      ls = t.booking_set.all
      messages.success(request,"Rating submitted successfully")
      return render(request,'books_user.html',{"ls":ls,"username":current_user})
    else:
      messages.warning(request,"You are not authorized to access this page")
      return render(request,'login.html')
  else:
    current_user = request.user
    ls = booking.objects.filter(user__username=request.user)
    return render(request,'borrowed.html',{"ls":ls,"username":current_user})

def review(request,n):
  if request.user.is_anonymous:
    return render(request,'login.html')
  if request.method =='POST':
    ls1 = booking.objects.get(user__username=request.user,book__code=n)
    ls1.rating=request.POST.get('rew')
    ls1.save()
    b = book.objects.get(code=n)
    b.final_rating = ((float(b.final_rating)*float(b.rating_count))+float(ls1.rating))/(int(b.rating_count)+1)
    b.rating_count=b.rating_count+1
    b.save()
    messages.success(request,"rating submited successfully")
    return redirect("/user")
  else:
    if userinfo.objects.get(username=request.user).role=='student':
      current_user = request.user
      ls = booking.objects.get(book__code=n,user__username=request.user)
      messages.success(request,"enter rating and after it click submit")
      t="/"+str(n)+"/review"
      return render(request,'review.html',{"item":ls,"t":t,"n":n,"username":request.user}) 
    else:
      messages.warning(request,"You are not authorized to access this page")
      return render(request,'login.html')

def booklist(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method == 'POST':
    if request.POST.get('name')=="name":
      ls=book.objects.all().filter(name__contains=request.POST.get('search'))
      return render(request,'booklist.html',{"ls":ls,"username":request.user})
    elif request.POST.get('author')=="author":
      ls=book.objects.all().filter(author__contains=request.POST.get('search'))
      return render(request,'booklist.html',{"ls":ls,"username":request.user})
    elif request.POST.get('trending')=="trending":
      ls=book.objects.all().filter(final_rating__gte=3)
      return render(request,'booklist.html',{"ls":ls,"username":request.user})
    else:
      ls=book.objects.all().filter(genre__contains=request.POST.get('search'))
      return render(request,'booklist.html',{"ls":ls,"username":request.user})
  else:
    ls=book.objects.all
    return render(request,'booklist.html',{"ls":ls,"username":request.user})

def librarian(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif userinfo.objects.get(username=request.user).role=='l':
    t=userinfo.objects.get(username=request.user)
    return render(request,'librarian.html',{"t":t})
  else:
    return render(request,'login.html')

def pending(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method == 'POST':
    if request.POST.get("accept"):
      i = booking.objects.get(id=request.POST.get("accept"))
      messages.success(request,"Request Accepted Successfully")
      i.idate=date.today()
      i.edate=date.today() + timedelta(days=14)
      if i.book.currentuser=="none":
        b=book.objects.get(code=i.book.code)
        b.currentuser=i.user.username
        b.available="no"
        b.save()
        i.acceptance=True
        i.save()
        return redirect("/pending_requests")
      else:
        b=book.objects.get(code=i.book.code)
        b.available="no"
        b.waiting_no=int(b.waiting_no)+1
        b.save()
        i.waiting_no=int(b.waiting_no)
        i.acceptance=True
        i.save()
        return redirect("/pending_requests")
    else:
      i = booking.objects.get(id=request.POST.get("decline"))
      b=book.objects.get(code=i.book.code)
      messages.warning(request,"Request has been declined")
      if i.book.currentuser=="none":
        b.available="yes"
        b.save()
        i.delete()
        return redirect("/pending_requests")
      else:
        b.available="no"
        b.save()
        i.delete()
        return redirect("/pending_requests")
  elif userinfo.objects.get(username=request.user).role=='l':
    t=userinfo.objects.get(username=request.user)
    ls= booking.objects.all().filter(book__available="hold",acceptance=False) #~Q
    return render(request,'pending.html',{"t":t,"ls":ls})
  else:
    return render(request,'login.html')

def dues(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method == 'POST':
    if request.POST.get("accept"):
      i = booking.objects.get(id=request.POST.get("accept"))
      messages.success(request,"Book Returned Successfully")
      b=book.objects.get(code=i.book.code)
      if i.book.waiting_no==0:
        b.available="yes"
        b.currentuser="none"
        b.save()
        i.delete()
        return redirect("/dues")
      else:
        new = booking.objects.get(waiting_no=i.book.waiting_no,book__name=i.book.name)
        b = book.objects.get(code=i.book.code)
        b.waiting_no=int(b.waiting_no)-1
        b.currentuser=new.user.username
        b.save()
        i.delete()
        return redirect("/dues")
  elif userinfo.objects.get(username=request.user).role=='l':
    t=userinfo.objects.get(username=request.user)
    ls= booking.objects.all().filter(acceptance=True) #~Q
    return render(request,'dues.html',{"t":t,"ls":ls})
  else:
    return render(request,'login.html')

def addbook(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method == "POST":
    code = int(request.POST.get('code'))
    name = request.POST.get('name')
    author = request.POST.get('author')
    isbn = request.POST.get('isbn')
    summary = request.POST.get('summary')
    genre = request.POST.get('genre')
    info = book(name=name,code=code,isbn=isbn,author=author,summary=summary,genre=genre)
    info.save()
    messages.success(request,"Book Created successfully")
    return render(request,'addbook.html')
  elif userinfo.objects.get(username=request.user).role=='l':
    return render(request,'addbook.html')
  else:
    return render(request,'login.html')

def alterbook(request):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method == "POST":
    if request.POST.get('name')=="name":
      ls=book.objects.all().filter(name__contains=request.POST.get('search'))
      return render(request,'alterbook.html',{"ls":ls,"username":request.user})
    elif request.POST.get('author')=="author":
      ls=book.objects.all().filter(author__contains=request.POST.get('search'))
      return render(request,'alterbook.html',{"ls":ls,"username":request.user})
    elif request.POST.get('genre')=="genre":
      ls=book.objects.all().filter(genre__contains=request.POST.get('search'))
      return render(request,'alterbook.html',{"ls":ls,"username":request.user})
    elif request.POST.get('delete'):
      b=book.objects.get(code=request.POST.get('delete'))
      b.delete()
      messages.success(request,"Book deleted successfully")
      return redirect("/alterbook")
    elif request.POST.get('modify'):
      i=request.POST.get('modify')
      i="/"+str(i)+"/modifyform"
      return redirect(i)
  elif userinfo.objects.get(username=request.user).role=='l':
      ls=book.objects.all
      return render(request,'alterbook.html',{"ls":ls,"username":request.user})
  else:
    return render(request,'login.html')

def modifyform(request,n):
  if request.user.is_anonymous:
    return render(request,'login.html')
  elif request.method=='POST':
    b=book.objects.get(code=n)
    b.name=request.POST.get("name")
    b.author=request.POST.get("author")
    b.isbn=request.POST.get("isbn")
    b.publisher=request.POST.get("publisher")
    b.summary=request.POST.get("summary")
    b.genre=request.POST.get("genre")
    b.save()
    i="/"+str(n)+"/modifyform"
    messages.success(request,"Book Details altered successfully")
    return redirect(i)
  elif userinfo.objects.get(username=request.user).role=='l':
    ls = book.objects.get(code=n)
    messages.warning(request,"feilds have been auto-filled, modify the required ones and submit")
    return render(request,'modifyform.html',{"ls":ls,"username":request.user})
  else:
    return render(request,'login.html')
