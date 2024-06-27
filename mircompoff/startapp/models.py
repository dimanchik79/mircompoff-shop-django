from django.db import models
from django.contrib.auth.models import User


def product_image_path(instance: "Product", filename: str) -> str:
    return "products/preview_{pk}/{filename}".format(pk=instance.pk, filename=filename)


def catalog_image_path(instance: "Catalog", filename: str) -> str:
    return "catalog/prewiew_{pk}/images_{pk}/{filename}".format(pk=instance.pk, filename=filename)


# class Profile(models.Model):
#     name_f = models.CharField(null=True, verbose_name="Фамилия", max_length=250)
#     name_i = models.CharField(null=True, verbose_name="Имя", max_length=250)
#     name_o = models.CharField(null=True, verbose_name="Отчество", max_length=250)
#     phone = models.CharField(null=True, verbose_name="Телефон", max_length=25)
#     adress = models.TextField(null=True, verbose_name="Место доставки")
#     email = models.EmailField(null=True, verbose_name="Электронная почта")
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class Catalog(models.Model):
    """Класс описывает модель Catalog (каталог товаров)"""
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата/время")
    name = models.CharField(null=False, max_length=100, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    preview = models.ImageField(null=True, blank=True, upload_to=catalog_image_path)
    softdelete = models.BooleanField(default=False, verbose_name="Пометить на удаление")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "каталог"
        verbose_name_plural = "каталог"


class Product(models.Model):
    """Класс описывает модель Products (товары)"""
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата/время")
    name = models.CharField(null=False, max_length=100, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    cost = models.DecimalField(null=False, max_digits=8, decimal_places=2, verbose_name="Цена")
    quantity = models.IntegerField(default=0, blank=True, verbose_name="В наличии")
    discount = models.IntegerField(default=0, blank=True, verbose_name="Скидка")
    preview = models.ImageField(null=True, blank=True, upload_to=product_image_path)
    softdelete = models.BooleanField(default=False, verbose_name="Пометить на удаление")

    # Связи
    catalog = models.ForeignKey(Catalog, on_delete=models.PROTECT, verbose_name="Каталог")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товар"

    def __str__(self) -> str:
        return f"(id={self.pk}) {self.name} (c={self.cost}, (q={self.quantity}), (d={self.discount}))"


class ProductReview(models.Model):
    """Класс описывает модель ProductReviews (отзывы о товаре)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата/время")
    review = models.TextField(blank=True, verbose_name="Отзыв")
    star = models.DecimalField(default=5, decimal_places=2, max_digits=5, null=False, verbose_name="Оценка")

    # Связи
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, null=False, verbose_name="Пользователь")

    def __str__(self):
        return (f"{self.review[:100] + '...' if len(self.review) > 100 else self.review} "
                f"- {self.reviewer} - star {self.star}")

    class Meta:
        verbose_name = "отзывы"
        verbose_name_plural = "отзывы"


class ProductImage(models.Model):
    """Класс описывает модель ProductsImage"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to=product_image_path)


class Basket(models.Model):
    """Класс описывает модель Catalog (каталог товаров)"""

    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата/время")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=False, verbose_name="Товар")
    quantity = models.IntegerField(default=1, blank=True, verbose_name="Количество")
    discount = models.IntegerField(default=0, blank=True, verbose_name="Скидка")
    cost = models.DecimalField(null=False, max_digits=10, decimal_places=2, verbose_name="Конечная стоимость")
    session_key = models.CharField(max_length=32, blank=True, verbose_name="Незарегистрированный пользователь")
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, verbose_name="Пользователь")
    ordered = models.BooleanField(default=False, verbose_name="Товар оформлен")
    softdelete = models.BooleanField(default=False, verbose_name="Пометить на удаление")

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзина"


# class Orders(models.Model):
#     """Класс описывает модель Order"""
#     delivery_adress = models.TextField(null=False, verbose_name="Адрес доставки")
#     promocode = models.CharField(blank=True, verbose_name="Промокод", max_length=25)
#     date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
#     user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
#     product = models.ManyToManyField(Products, related_name="orders", verbose_name="Товары")
#     receipt = models.FileField(null=True, upload_to="oders/receipts/", verbose_name="Файл с чеком")
#
#     def __str__(self) -> str:
#         return f"Order id={self.pk} for User={self.user}, date/time={self.date}"
