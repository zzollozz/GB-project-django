from django.db import models
from django.conf import settings

from mainapp.models import Product

from django.utils.functional import cached_property

class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    def __str__(self):
        return f"{self.product}, {self.quantity}"

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
        ordering = ('created_at',)

    """ Следующий код (ф-ции) лучше писать в СЕРВИСНОЙ МОДЕЛИ в Джанго !!!? """

    @cached_property
    def get_items_cached(self):
        """ Создаем кеш корзины """
        return self.user.basket_set.select_related()

    @property
    def product_cost(self):     # Стоимость продукта
        """ Метод при получении стоимости КорзинкИ """
        return self.product.price * self.quantity

    @property
    def total_quantity(self):   # Общая численность
        # _items = Basket.objects.filter(user=self.user)
        # # return sum(list(map(lambda x: x.quantity, _items)))
        # return sum(list(_items.values_list('quantity', flat=True)))
        """ после как создали Кеш """
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):       # Общая стоимость
        # _items = Basket.objects.filter(user=self.user)
        # return sum(list(map(lambda x: x.product_cost, _items)))
        """ после как создали Кеш """
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)
