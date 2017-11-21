from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from goldbook.models import Book


def index(request):
    return render(request, 'home.html')

@csrf_exempt
def search(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        books = Book.objects.filter(Q(book_name__icontains=key) |Q(book_isbn__icontains=key))
        return render(request,'search.html',{'books':books})
