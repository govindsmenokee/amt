from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	
	
	return render_to_response("homepage/index.html", {}, RequestContext(request))


