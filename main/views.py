from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import json
import random

# Create your views here.
def get_books(request):
    mybook={1:"hbo",2:"reunbo",3:"r-bo"}

    return HttpResponse(json.dumps(mybook))

def index(request):
    now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(f'<h1>現在時刻:{now}</h1>')

def lottory(request):
    numbers=sorted(random.sample(range(1,49),6))
    x=random.randint(1,49)
    number_str=' '.join(map(str,numbers))
    return render(request,'lottory.html',{"numbers":number_str,"x":x})

def lottory_2(request):
    numbers=sorted(random.sample(range(1,49),6))
    x=random.randint(1,49)
    number_str=' '.join(map(str,numbers))
    return HttpResponse(f'<h1>號碼:{number_str}特別號:{x}</h1>')