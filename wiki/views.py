from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from wiki.models import Page
from django.http import JsonResponse
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
def api_all(request):
	fill = {}
	lt = []
	ct=[]
	page = Page.objects.all()
	for i in page:
		lt.append(i.name)
	fill['title'] = lt
	return JsonResponse(fill)
def api_page(request,page_name):
	page = Page.objects.all()
	fill1={}
	for j in page:
		if j.name==page_name:
			fill1['content']=j.content
	return JsonResponse(fill1)
def delete_page(request,page_name):
	msg={}
	try:
		page = Page.objects.get(pk=page_name)
		page.delete()
		msg["status"]="200 OK"
	except Page.DoesNotExist:
		msg["status"]="404 Error"
		

	return JsonResponse(msg)
def add_details(request,page_name):
	msg={}
	if request.method == 'POST':
		content = request.POST.get("content","")
		try:
			page = Page.objects.get(pk=page_name)
			page.content = content
			msg["status"]="200 OK"
		except Page.DoesNotExist:
			page = Page(name=page_name, content= content)
			msg["status"]="201 Empty"
		page.save()
	else:
		msg["status"] = "202 Invalid"
	return JsonResponse(msg)

