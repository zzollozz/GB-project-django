from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"#{self.pk}. {self.name}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name', )    # Индексация по нужному полю # Сортировка по какому полю


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name='Изображение')
    shot_desc = models.CharField(max_length=255, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"{self.name}. {self.category.name}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
