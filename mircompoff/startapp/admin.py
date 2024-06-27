from django.contrib import admin

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet, Avg
from django.urls import path
from django.utils.safestring import mark_safe

from .models import Product, Catalog, ProductImage, ProductReview, Basket


@admin.action(description="Пометить на удаление")
def mark_softdelete(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archive=True)


@admin.action(description="Убрать пометку на удаление")
def mark_unsoftdelete(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archive=False)


class ProductsImagesInline(admin.TabularInline):
    """Класс описывает сущность ProductsImagesInline"""
    model = ProductImage
    extra = 1


class ProductReviewInline(admin.TabularInline):
    """Класс описывает сущность ProductReviewInline"""
    model = ProductReview
    extra = 1


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    """Класс описывает сущность ProductsAdmin"""
    actions = [mark_softdelete, mark_unsoftdelete]
    inlines = [ProductReviewInline, ProductsImagesInline]
    list_display = (
        "pk", "date", "catalog", "name", "quantity", "cost", "description_short", "discount", "get_stars", "softdelete")
    list_display_links = "pk", "name", "description_short"
    ordering = ("pk",)
    search_fields = "name", "catalog", "cost"
    list_editable = ("softdelete",)
    list_filter = ("softdelete", "date")
    fieldsets = [
        ("Опции товара", {
            "fields": ("name", "description", "catalog")}),
        ("Изображение", {"fields": ("preview",)}),
        ("Цена и остаток", {"fields": ("cost", "discount", "quantity")}),
        ("Мягкое удаление",
         {"fields": ("softdelete",), "classes": ("collapse",), "description": "Пометить продукт для удаление"}),
    ]

    @admin.display(description="Краткое описание")
    def description_short(self, obj: Product) -> str:
        """Метод возвращает короткую строку для поля description"""
        if len(obj.description) < 48:
            return f"{obj.description}"
        else:
            return f"{obj.description[:45]}..."

    @admin.display(description="Средняя оценка")
    def get_stars(self, product: Product):
        star = ProductReview.objects.filter(product_id=product.pk).aggregate(Avg('star'))
        return f"{round(star['star__avg'], 1)} звезд(ы)"


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    """Класс описывает сущность CatalogAdmin"""
    actions = [mark_softdelete, mark_unsoftdelete]
    list_display = "pk", "date", "name", "description_short", "image_show", "softdelete"
    list_display_links = "pk", "name", "description_short"
    ordering = ("pk",)
    search_fields = "date", "name", "description"
    list_editable = ("softdelete",)
    list_filter = ("softdelete", "date")
    fieldsets = [
        ("Опции каталога", {"fields": ("name", "description",)}),
        ("Изображение", {"fields": ("preview",)}),
    ]

    @admin.display(description="Краткое описание")
    def description_short(self, obj: Product) -> str:
        """Метод возвращает короткую строку для поля description"""
        if len(obj.description) < 48:
            return f"{obj.description}"
        else:
            return f"{obj.description[:45]}..."

    @admin.display(description="Превью")
    def image_show(self, obj):
        if obj.preview:
            return mark_safe(f"<img src='{obj.preview.url}' width='75' height='75'/>")
        else:
            return "None"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Класс описывает сущность ProductRewiew"""
    list_display = "pk", "date", "review_short", "star", "reviewer", "get_product"
    list_display_links = "pk", "review_short"
    ordering = ("pk",)
    search_fields = "review",

    @admin.display(description="Отзыв")
    def review_short(self, obj: ProductReview) -> str:
        """Метод возвращает короткую строку для поля description"""
        if len(obj.review) < 48:
            return f"{obj.review}"
        else:
            return f"{obj.review[:45]}..."

    @admin.display(description="Товар")
    def get_product(self, prooductreview: ProductReview):
        product_name = Product.objects.get(pk=prooductreview.product_id)
        return product_name


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """Класс описывает сущность BasketAdmin"""
    list_display = "pk", "date", "get_product", "quantity", "discount", "cost", "user", "ordered", "softdelete"
    list_display_links = "pk", "date", "get_product"
    ordering = ("pk", )
    search_fields = "user",
    list_editable = ("softdelete", )
    list_filter = ("softdelete", "date", "user", )

    @admin.display(description="Товар")
    def get_product(self, product: Product):
        product_name = Product.objects.get(pk=product.product_id)
        return product_name
