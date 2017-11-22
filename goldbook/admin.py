from django.contrib import admin

# Register your models here.
from goldbook.models import Book, Author, Publisher, Eplatform, PlatBookInfo


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_isbn','book_name','get_authors','book_retail_price','book_pub_date','book_douban_score')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name','author_name_en',)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_name',)

class EplatformAdmin(admin.ModelAdmin):
    list_display = ('plat_code','plat_name','plat_icon')

class PlatBookInfoAdmin(admin.ModelAdmin):
    list_display = ('book','plat','product_id','book_price','book_url','book_update_time')
    list_filter = ('plat',)

admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Eplatform,EplatformAdmin)
admin.site.register(PlatBookInfo,PlatBookInfoAdmin)