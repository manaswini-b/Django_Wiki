from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from wiki.models import Page
from django.http import JsonResponse
from django.shortcuts import render
from django import 	forms as forms
# Create your views here.


def find_cate():
	cate = []
	page = Page.objects.all()
	for i in page:
		cate.append(i.cate)
	seen = set()
	seen_add = seen.add
	return [x for x in cate if not (x in seen or seen_add(x))]

class SearchForms(forms.Form):
	text = forms.CharField(label = "Enter search term")

def search_page(request):
	if request.method == "POST":
		f = SearchForms(request.POST)
		if not f.is_valid():
			return render_to_response("search.html",{"form":f})
		else:
			pages = Page.objects.filter(name__contains = f.cleaned_data["text"].replace("?","__").replace("/","^^"))
			contents = Page.objects.filter(content__contains = f.cleaned_data["text"]) 
			for i in range(len(pages)): 
				pages[i].name = pages[i].name.replace("__","?").replace("^^","/")
			for i in range(len(contents)): 
				contents[i].name = contents[i].name.replace("__","?").replace("^^","/")
			return render_to_response("search.html",{"form":f,"pages":pages,"contents":contents})
	f = SearchForms()
	return render_to_response("search.html",{"form":f})

def view_page(request, page_name):
	try:
		page=Page.objects.get(pk=page_name)
	except Page.DoesNotExist:
		return render_to_response("create.html",{"page_name":page_name.replace("__","?").replace("^^","/")})
	content = page.content
	return render_to_response("view.html",{"page_name":page_name.replace("__","?").replace("^^","/"),"content":content,"cate": page.cate})
def edit_page(request,page_name):
	try:
		page = Page.objects.get(pk=page_name)
		content = page.content
		cate = page.cate
	except Page.DoesNotExist:
		content = "" 
		cate =""
	return render_to_response("edit.html",{"page_name":page_name.replace("__","?").replace("^^","/"),"content":content,"data":find_cate()})

def cate_page(request,page_name):
	pages = []
	pages = Page.objects.filter(cate__contains=page_name)
	for i in range(len(pages)): 
		pages[i].name = pages[i].name.replace("__","?").replace("^^","/")
	return render_to_response("cate_browse.html",{"page_name":page_name.replace("__","?").replace("^^","/"),"data":pages})

def save_page(request,page_name):
	content = request.POST.get("content","")
	cate = request.POST.get("cate","")
	try:
		page = Page.objects.get(pk=page_name.replace("?","__").replace("/","^^"))
		page.content = content
		page.cate = cate
	except Page.DoesNotExist:
		page = Page(name=page_name.replace("?","__").replace("/","^^"), content= content, cate = cate)
	page.save()
	return HttpResponseRedirect("/wiki/"+page_name+"/")

def browse_page(request):
	pages = Page.objects.all() 
	for i in range(len(pages)): 
		pages[i].name = pages[i].name.replace("__","?").replace("^^","/")
	return render(request, 'browse.html',{'data': pages,"cate": find_cate()})

def index_page(request):
	return render_to_response('index.html')

def add_page(request):
	return render_to_response("add.html",{"error":"","data": find_cate()})
def save_add(request):
	content = request.POST.get("content","")
	page_name = request.POST.get("page_name","")
	cate = request.POST.get("cate","")
	try:
		page = Page.objects.get(pk=page_name.replace("?","__").replace("/","^^"))
		return render_to_response("add.html",{"error":"Name already exist"})
	except Page.DoesNotExist:
		page = Page(name=page_name.replace("?","__").replace("/","^^"), content= content, cate = cate)
		page.save()
		return HttpResponseRedirect("/browse")
def api_all(request):
	fill = {}
	lt = []
	ct=[]
	page = Page.objects.all()
	for i in page:
		lt.append(i.name.replace("__","?").replace("^^","/"))
	fill['title'] = lt
	return JsonResponse(fill)
def api_page(request,page_name):
	page = Page.objects.all()
	fill1={}
	for j in page:
		if j.name==page_name:
			fill1['content']=j.content
			fill1['cate']=j.cate
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
		cate = request.POST.get("cate","")
		try:
			page = Page.objects.get(pk=page_name)
			page.content = content
			page.cate = cate
			msg["status"]="200 OK"
		except Page.DoesNotExist:
			page = Page(name=page_name, content= content , cate = cate)
			msg["status"]="201 Empty"
		page.save()
	else:
		msg["status"] = "202 Invalid"
	return JsonResponse(msg)

