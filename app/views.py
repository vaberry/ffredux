from django.shortcuts import render

# Create your views here.
from django.views import View

class Base(View):
    def get(self,request,*args,**kwargs):
        return render(request,'app/base.html')

class Home(View):
    def get(self,request,*args,**kwargs):
        return render(request,'app/home.html')