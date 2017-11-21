from django.contrib import admin

# Register your models here.
from goldbook.models import Book, Author, Publisher


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_isbn','book_name','book_retail_price','book_pub_date','book_douban_score')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name','author_name_en',)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_name',)

admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Publisher,PublisherAdmin)