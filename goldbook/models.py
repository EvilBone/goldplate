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
    plat_icon = models.ImageField(verbose_name='图标')

    class Meta:
        verbose_name = '电商平台'
        verbose_name_plural = '电商平台'

    def __str__(self):
        return self.plat_name

class PlatPrice:
    def __init__(self,plat='',price=0,link=''):
        self.plat = plat
        self.price = price
        self.link = link

class Book_AM(models.Model):
    TYPE_CHOICES = (
        (1, u'平装'),
        (2, u'精装'),
        (2, u'Kindle'),
    )
    am_isbn = models.CharField(max_length=50,validators='ISBN',null=True,blank=True)
    am_name = models.CharField(max_length=500,verbose_name='书名',null=True,blank=True)
    am_pub = models.CharField(max_length=200,verbose_name='出版信息',null=True,blank=True)
    am_kindle  = models.BooleanField(verbose_name='Kindle',default=False)
    am_uti_kindle = models.BooleanField(verbose_name='Kindle Unlimited',default=False)
    am_kindle_pirce = models.FloatField(verbose_name='Kindle价格',null=True,blank=True)
    am_paper_price = models.FloatField(verbose_name='纸质价格',null=True,blank=True)
    am_type = models.IntegerField(verbose_name='装帧',null=True,blank=True,choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'am书'
        verbose_name_plural='am书'

class URLManager(models.Model):
    STAT_CHOICES = (
        (0, u'初始'),
        (1, u'等待'),
        (2, u'下载中'),
        (3, u'完成'),
        (4, u'异常'),
    )
    web_url = models.CharField(max_length=1000,verbose_name='URL')
    web_plate = models.ForeignKey(Eplatform,verbose_name='平台')
    handle_stat = models.IntegerField(verbose_name='处理状态',choices=STAT_CHOICES,default=0)
    handle_time = models.DateTimeField(verbose_name='处理时间',auto_now=True)
    handle_message = models.TextField(verbose_name='处理结果',null=True,blank=True)

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URL'


# 书
class Book(models.Model):
    book_isbn = models.CharField(max_length=20, verbose_name='ISBN')
    book_name = models.CharField(max_length=200, verbose_name='书名')
    book_retail_price = models.FloatField(verbose_name='定价')
    book_author = models.ManyToManyField(Author, verbose_name='作者', blank=True)
    book_pub = models.ManyToManyField(Publisher, verbose_name='出版社', blank=True)
    book_pub_date = models.CharField(max_length=100, verbose_name='出版日期', null=True, blank=True)
    book_imageurl = models.URLField(verbose_name='图片')
    book_binding = models.CharField(max_length=100, verbose_name='装帧', blank=True, null=True)
    book_douban_score = models.FloatField(verbose_name='豆瓣评分', blank=True, null=True)
    book_create_time = models.DateTimeField(verbose_name='添加时间', auto_created=True, auto_now_add=True)
    book_douban_url = models.URLField(verbose_name='豆瓣链接',default='')
    book_is_update_jd= models.BooleanField(verbose_name='是否更新',default=False)
    book_is_update_dd = models.BooleanField(verbose_name='是否更新', default=False)

    def get_lowest_price(self):
        jdplat = PlatPrice()
        if len(PlatBookInfo.objects.filter(book=self))>0:
            platinfo = PlatBookInfo.objects.filter(book=self).order_by('book_price')[0]
            jdplat.plat = platinfo.plat.plat_code
            jdplat.link = platinfo.book_url
            jdplat.price = platinfo.book_price
        else:
            jdplat.price = self.book_retail_price
        return jdplat

    def get_lowest_list(self):
        list = []
        if len(PlatBookInfo.objects.filter(book=self,plat__plat_code='jd'))>0:
            jdplat = PlatPrice()
            platinfo = PlatBookInfo.objects.filter(book=self,plat__plat_code='jd').order_by('book_price')[0]
            jdplat.plat = platinfo.plat.plat_code
            jdplat.link = platinfo.book_url
            jdplat.price = platinfo.book_price
            list.append(jdplat)
        if len(PlatBookInfo.objects.filter(book=self,plat__plat_code='dd'))>0:
            jdplat = PlatPrice()
            platinfo = PlatBookInfo.objects.filter(book=self,plat__plat_code='dd').order_by('book_price')[0]
            jdplat.plat = platinfo.plat.plat_code
            jdplat.link = platinfo.book_url
            jdplat.price = platinfo.book_price
            list.append(jdplat)
        return list

    def get_authors(self):
        s = ''
        for a in self.book_author.all():
            s += a.author_name + ' ，'
        return s[0:-1]

    get_authors.short_description = u"作者"

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
    plat = models.ForeignKey(Eplatform,verbose_name='平台')
    product_id = models.CharField(max_length=50,verbose_name='商品编号')
    book = models.ForeignKey(Book,verbose_name='书名')
    book_price = models.FloatField(verbose_name='平台价格', null=True, blank=True, default=0)
    book_url = models.URLField(verbose_name='商品链接', null=True, blank=True)
    book_update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '价格信息'
        verbose_name_plural = '价格信息'
