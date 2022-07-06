from pydoc import Doc
from django.shortcuts import render,redirect

# Create your views here.
from django.views import View
from .models import NewDocument
from .forms import DocumentForm

class Base(View):
    def get(self,request,*args,**kwargs):
        pics = NewDocument.objects.all()

        context = {
            'pics': pics,
        }

        print('PICCCC',pics)

        return render(request,'app/base.html', context)

class Home(View):
    def get(self,request,*args,**kwargs):
        form = DocumentForm()
        pics = NewDocument.objects.all()
        
        context = {
            'pics': pics,
            'form': form,
        }


        return render(request,'app/home.html',context)

    def post(self,request,*args,**kwargs):

        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DocumentForm()

            context = {
                'form': form,
            }

        return render(request,'app/home.html',context)