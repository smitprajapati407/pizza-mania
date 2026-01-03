from django.shortcuts import render
from store.models import Category,Pizaa


def home(request):
    categories= Category.objects.all()
    return render(request,'home.html',{'categories': categories})


def Menu(request):
    categories=Category.objects.all()
    pizaas=Pizaa.objects.all()

    category_id=request.GET.get('category')
    if category_id:
        pizaas=pizaas.filter(category_id=category_id)

    return render(request, 'menu.html',{"categories":categories,"pizaas":pizaas})    

# Create your views here.
