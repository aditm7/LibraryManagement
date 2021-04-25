from django.db import models

# Create your models here

class userinfo(models.Model):
  hostel = models.CharField(max_length=100,blank=True,default='')
  role = models.CharField(max_length=100,default='student',choices=[("student","Student"),("l","Librarian")])
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100,default='')
  username = models.CharField(max_length=100,primary_key=True)
  year = models.CharField(max_length=100,blank=True,default='')
  def __str__(self):
    return self.username

class book(models.Model):
  code = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=100)
  author = models.CharField(max_length=100,default='')
  isbn = models.CharField(max_length=100)
  genre = models.CharField(max_length=100,default='')
  publisher = models.CharField(max_length=200,default='')
  summary = models.CharField(max_length=100000,default='')
  final_rating = models.DecimalField(max_digits=2, decimal_places=1,default='0')
  available = models.CharField(max_length=100,choices=[('yes','Available'),('no','In waiting'),('hold','Currently in hold')],default='yes') #can take hold,yes,no
  waiting_no =models.IntegerField(default='0')
  rating_count = models.IntegerField(default='0')
  currentuser = models.CharField(max_length=1000,default='none')

  def __str__(self):
    return self.name

class booking(models.Model):
  user = models.ForeignKey(userinfo,on_delete=models.CASCADE)
  book = models.ForeignKey(book,on_delete=models.CASCADE)
  rating = models.DecimalField(max_digits=2, decimal_places=1,default='0')
  idate = models.DateField()
  edate = models.DateField()
  acceptance = models.BooleanField(default=False)
  waiting_no = models.IntegerField(default=0)
