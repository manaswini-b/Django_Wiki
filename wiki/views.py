from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from wiki.models import Page
from django.shortcuts import render
# Create your views here.
def view_page(request, page_name):
	try:
		page=Page.objects.get(pk=page_name)
	except Page.DoesNotExist:
		return render_to_response("create.html",{"page_name":page_name})
	content = page.content
	return render_to_response("view.html",{"page_name":page_name,"content":content})
def edit_page(request,page_name):
	try:
		page = Page.objects.get(pk=page_name)
		content = page.content
	except Page.DoesNotExist:
		content = ""
	return render_to_response("edit.html",{"page_name":page_name,"content":content})
def save_page(request,page_name):
	content = request.POST.get("content","")
	try:
		page = Page.objects.get(pk=page_name)
		page.content = content
	except Page.DoesNotExist:
		page = Page(name=page_name, content= content)
	page.save()
	return HttpResponseRedirect("/wiki/"+page_name+"/")
def index_page(request):
	page = Page.objects.all()
	return render(request, 'index.html',{'data': page})
def add_page(request):
	return render_to_response("add.html",{"error":""})
def save_add(request):
	content = request.POST.get("content","")
	page_name = request.POST.get("page_name","")
	try:
		page = Page.objects.get(pk=page_name)
		return render_to_response("add.html",{"error":"Name already exist"})
	except Page.DoesNotExist:
		page = Page(name=page_name, content= content)
		page.save()
		return HttpResponseRedirect("/")