from django.db import models



class ProductCategory(models.Model):

    name = models.CharField(verbose_name='название категории', unique=True, max_length=128)
    description = models.CharField(verbose_name='описание категории', blank=True, max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(db_index=True, default=False)

    def __str__(self):
        return self.name or f'Category id - {self.pk}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название продукта', max_length=128, unique=True)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_deleted = models.BooleanField(db_index=True, default=False)

    @staticmethod
    def get_items():
        return Product.objects.filter(is_deleted=False).order_by('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    # def get_absolute_url(self):
    #     return reverse('admin_staff:products', args=[self.pk])

