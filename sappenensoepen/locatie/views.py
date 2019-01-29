 # locatie/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.http import HttpResponse
import sqlite3
# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT name FROM steden')
        steden = c.fetchall()
        adreslist = ""
        for i in steden:
        	if i[0] == "Utrecht (gemeente)":
        		adreslist += "Utrecht,"
        	else:
	        	adreslist += i[0] + ","
        adreslist = adreslist[:-1]
        return render(request, 'index.html', { "adreslist": adreslist })

