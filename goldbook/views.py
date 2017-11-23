from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from goldbook.models import Book


def index(request):
    return render(request, 'home.html')


@csrf_exempt
def search(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key is None or key == '':
            return HttpResponseRedirect("/")
        else:
            allbooks = Book.objects.filter(
                Q(book_name__icontains=key) | Q(book_isbn__icontains=key) | Q(book_author__author_name__contains=key))
        count = len(allbooks)
        paginator = Paginator(allbooks, 25)
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            books = paginator.page(paginator.num_pages)
        return render(request, 'search.html', {'books': books,'key':key,'count':count})
