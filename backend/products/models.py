from django.db import models
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=250,unique=True,verbose_name="Nom")
    slug=models.SlugField(max_length=250,unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_list")


class Product(models.Model):
    name=models.CharField(max_length=250,verbose_name="Nom")
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Prix")
    stock=models.PositiveIntegerField(default=0,verbose_name=" quantite en Stock")
    category=models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name="Categorie"
    )
    image=models.FileField(null=True, blank=True, upload_to='products/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk])
