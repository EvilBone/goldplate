from django.contrib import admin

# Register your models here.
from goldbook.models import Book, Author, Publisher, Eplatform, PlatBookInfo, Book_AM, URLManager


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_isbn','book_name','get_authors','book_retail_price','book_pub_date','book_douban_score')
    search_fields = ('book_isbn','book_name')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name','author_name_en',)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_name',)

class EplatformAdmin(admin.ModelAdmin):
    list_display = ('plat_code','plat_name','plat_icon')

class PlatBookInfoAdmin(admin.ModelAdmin):
    list_display = ('book','plat','product_id','book_price','book_url','book_update_time')
    list_filter = ('plat',)
    search_fields = ('book','isbn')

class AMBookAdmin(admin.ModelAdmin):
    list_display = ('am_isbn','am_name','am_pub','am_kindle','am_uti_kindle','am_kindle_pirce','am_paper_price','am_type')

    list_filter = ('am_type',)

class URLManagerAdmin(admin.ModelAdmin):
    list_display = ('web_url','web_plate','handle_stat','handle_time','handle_message')

    list_filter = ('handle_stat',)

admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Eplatform,EplatformAdmin)
admin.site.register(PlatBookInfo,PlatBookInfoAdmin)
admin.site.register(Book_AM,AMBookAdmin)
admin.site.register(URLManager,URLManagerAdmin)