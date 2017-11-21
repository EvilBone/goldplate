from django.db import models


# Create your models here.
# 作者
class Author(models.Model):
    author_name = models.CharField(max_length=100, verbose_name='姓名')
    author_name_en = models.CharField(max_length=100, verbose_name='英文姓名', null=True, blank=True)

    class Meta:
        verbose_name_plural = '作者'
        verbose_name = '作者'

    def __str__(self):
        return self.author_name


# 出版社
class Publisher(models.Model):
    publisher_name = models.CharField(max_length=200, verbose_name='出版社名称')

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = '出版社'

    def __str__(self):
        return self.publisher_name


# 电商平台
class Eplatform(models.Model):
    plat_code = models.CharField(max_length=5, verbose_name='平台代码')
    plat_name = models.CharField(max_length=20, verbose_name='平台名称')

    class Meta:
        verbose_name = '电商平台'
        verbose_name_plural = '电商平台'

    def __str__(self):
        return self.plat_name


# 书
class Book(models.Model):
    book_isbn = models.CharField(max_length=20, verbose_name='ISBN')
    book_name = models.CharField(max_length=200, verbose_name='书名')
    book_retail_price = models.FloatField(verbose_name='定价')
    book_author = models.ManyToManyField(Author, verbose_name='作者', blank=True)
    book_pub = models.ManyToManyField(Publisher, verbose_name='出版社', blank=True)
    book_pub_date = models.CharField(max_length=10, verbose_name='出版日期', null=True, blank=True)
    book_imageurl = models.URLField(verbose_name='图片')
    book_binding = models.CharField(max_length=25, verbose_name='装帧', blank=True, null=True)
    book_douban_score = models.FloatField(verbose_name='豆瓣评分', blank=True, null=True)
    book_create_time = models.DateTimeField(verbose_name='添加时间', auto_created=True, auto_now_add=True)
    book_douban_url = models.URLField(verbose_name='豆瓣链接',default='')

    def get_lowest_price(self):
        if len(PlatBookInfo.objects.filter(book=self))>0:
            platprice = PlatBookInfo.objects.filter(book=self).order_by('book_price')[0].book_price
        else:
            platprice = self.book_retail_price
        return platprice

    def get_authors(self):
        s = ''
        for a in self.book_author.all():
            s += a.author_name + ' ，'
        return s[0:-1]

    def get_pubs(self):
        s = ''
        for a in self.book_pub.all():
            s += a.publisher_name + ' ，'
        return s[0:-1]

    def __str__(self):
        return self.book_name

    class Meta:
        verbose_name = '书'
        verbose_name_plural = '书'


# 平台上书的信息
class PlatBookInfo(models.Model):
    plat = models.ForeignKey(Eplatform)
    book = models.ForeignKey(Book)
    book_price = models.FloatField(verbose_name='平台价格', null=True, blank=True, default=0)
    book_url = models.URLField(verbose_name='商品链接', null=True, blank=True)
    book_update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '价格信息'
        verbose_name_plural = '价格信息'
