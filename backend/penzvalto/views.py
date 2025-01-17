from django.shortcuts import render, redirect
from . models import Valutak, mnb_deviza, mnb_name
import requests
import datetime

from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import ValutakSerializer, MnbSerializer, MnbNameSerializer

from . import forms
from django.contrib.auth import login, logout, authenticate  # add to imports
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from . import mnb_deviza_download

@login_required
def home(request):

    valutak = Valutak.objects.all()
    context = {
        'mytitle': "Valutaváltó - Home page",
    }
        
    if request.method == "POST": # a valutaváltót működtető programrész
        atvaltando = float(request.POST.get('atvaltando',0))
        errol = request.POST.get('errol')
        erre = request.POST.get('erre')
        try: mirolertek = Valutak.objects.get(penznem=errol).arfolyam
        except Valutak.MultipleObjectsReturned: mirolertek = Valutak.objects.filter(penznem=errol).first().arfolyam
        try: mireertek = Valutak.objects.get(penznem=erre).arfolyam
        except Valutak.MultipleObjectsReturned: mireertek = Valutak.objects.filter(penznem=erre).first().arfolyam
        atvaltottertek= round(atvaltando * (mireertek / mirolertek))
        context = {
            'mytitle': "Valutaváltó - Home page",
            'valutak': valutak, 
            'atvaltottertek': atvaltottertek, 
            'errol': errol, 
            'erre': erre, 
            'atvaltando': atvaltando,
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html', context)

#-------------------------------------------------------------------------------------------------------------------------------------

# ha szeretnéd használni az adatbázisban lévő adatokat rest API-n keresztül, így hozzáférhetsz
@api_view(['GET'])
def restAdatKezeles(request):
    if request.method == "GET":
        allData=Valutak.objects.all()
        serialized=ValutakSerializer(allData, many=True) 
        #return JsonResponse(serialized.data, safe=False)
        return Response(serialized.data)

@api_view(['GET'])
def restMNBValuta(request):
    if request.method == "GET":
        allData = mnb_deviza.objects.filter(date__range=(datetime.datetime.now()-datetime.timedelta(days=30), datetime.datetime.now() ))
        serialized = MnbSerializer(allData, many=True) 
        return Response(serialized.data)


@api_view(['GET'])
def restMNBValutaLast(request):
    if request.method == "GET":
        last = mnb_deviza.objects.order_by("-date")[:1].values("date")
        allData = mnb_deviza.objects.filter(date = last )
        serialized = MnbSerializer(allData, many=True) 
        return Response(serialized.data)

@api_view(['GET'])
def restMNBName(request):
    if request.method == "GET":
        #mnb_deviza_download.nmbLetolt()
        allData = mnb_name.objects.all()
        serialized = MnbNameSerializer(allData, many=True) 
        return Response(serialized.data)

@api_view(['GET'])
def restMNBRefresh(request):
    if request.method == "GET":
        mnb_deviza_download.nmbLetolt()
        return redirect('login')




@api_view(['POST']) #valuta adatok lekérése REST API-val
def penzadatlekeres(request):
    response = requests.get('https://infojegyzet.hu/webszerkesztes/php/valuta/api/v1/arfolyam/')
    if response.status_code == 200:
        data = response.json()
        for penznem, arfolyam in data['rates'].items():
            Valutak.objects.update_or_create(
                penznem=penznem,
                defaults={'arfolyam': arfolyam}
            )
        return Response({'status': 'success', 'data': data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status': 'error', 'message': 'Penznemek lekérése sikertelen.'}, status=status.HTTP_400_BAD_REQUEST)


    
#-------------------------------------------------------------------------------------------------------------------------------------

#FELHASZNÁLÓ KEZELÉSHEZ SZÜKSÉGES METÓDUSOK:

def logout_user(request): #kijelentkezés
    logout(request)
    return redirect('login')

def login_page(request):#bejelentkezés
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                penzadatlekeres(request) #itt van meghívva a pénznem lekéréséért felelős rest függvény
                return redirect('home')
            else:
                message = 'Bejelentkezés sikertelen'
    return render(request, 'login.html', context={'form': form, 'message': message})

def signup_page(request): #regisztráció, illetve az épp regisztrált felhasználó automatikus bejelentkezése
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html', context={'form': form})

@login_required # éppen bejelentkezett felhasználó törlése (!!óvatosan használd, nehogy a superusert töröld!!)
def delete_user(request):
    user=request.user
    User.delete(user)
    return redirect('login')