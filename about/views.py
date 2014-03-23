from django.template import RequestContext
from django.shortcuts import render_to_response

def aboutpage(request):
	return render_to_response('about/index.html', {}, RequestContext(request))
