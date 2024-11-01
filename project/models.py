from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to="category-images/")

    class Meta:
        verbose_name = "Katalog"
        verbose_name_plural = "Kataloglar"

    def __str__(self) -> str:
        return self.name


class ProductSize(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "O'lcham"
        verbose_name_plural = "O'lchamlar"

    def __str__(self) -> str:
        return self.name


class ProductColor(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Rang"
        verbose_name_plural = "Ranglar"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(default=1)
    colors = models.ManyToManyField(ProductColor, blank=True, related_name="products")
    sizes = models.ManyToManyField(ProductSize, blank=True, related_name="products")

    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name

    def priceWithDiscount(self):
        return self.price - self.discount


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product-images/")


class AdditionalInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="infos")
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=128)
    email = models.EmailField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rate = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    text = models.TextField()

    def __str__(self) -> str:
        return self.full_name

    def get_range(self):
        return [1, 2, 3, 4, 5]