from django.shortcuts import render
from . models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request,c_slug=None):
    c_page=None
    prodt=None
    cat=None
    if c_slug!=None:
       c_page=get_object_or_404(categ,slug=c_slug)
       prodt=products.objects.filter(category=c_page,avaliable=True)
    else:

      prodt=products.objects.all().filter(avaliable=True)
      cat=categ.objects.all()
      # Set up paginator with 6 products per page
    paginator = Paginator(prodt, 6)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request,'index.html',{'pr':page_obj,'ct':cat})

def prodDetails(request, c_slug, product_slug):
    try:
        prod = products.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'item.html', {'pr': prod})

def searching(request):
    prod=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod = products.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))

    return render(request,'search.html',{'qr':query,'pr':prod})