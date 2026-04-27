from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView

from .data import list_products
from .forms import CategoryForm, ProductForm
from .models import Category, Product


class ProductListView(View):
    def get(self, request):
        db_products = Product.objects.select_related("category").all()

        if db_products.exists():
            products = db_products
            use_demo_data = False
        else:
            products = list_products
            use_demo_data = True

        return render(
            request,
            "products/product_list.html",
            {
                "products": products,
                "use_demo_data": use_demo_data,
            },
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(View):
    def get(self, request):
        return render(request, "products/product_form.html", {"form": ProductForm(), "title": "Ajouter un produit"})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit ajoute avec succes.")
            return redirect("product_list")
        return render(request, "products/product_form.html", {"form": form, "title": "Ajouter un produit"})


class ProductUpdateView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(
            request,
            "products/product_form.html",
            {"form": ProductForm(instance=product), "title": "Modifier le produit", "product": product},
        )

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifie avec succes.")
            return redirect("product_detail", pk=product.pk)
        return render(
            request,
            "products/product_form.html",
            {"form": form, "title": "Modifier le produit", "product": product},
        )


class ProductDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, "products/product_confirm_delete.html", {"product": product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, "Produit supprime avec succes.")
        return redirect("product_list")


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "products/category_list.html", {"categories": categories})


class CategoryCreateView(View):
    def get(self, request):
        return render(request, "products/category_form.html", {"form": CategoryForm(), "title": "Ajouter une categorie"})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categorie ajoutee avec succes.")
            return redirect("category_list")
        return render(request, "products/category_form.html", {"form": form, "title": "Ajouter une categorie"})


class CategoryUpdateView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(
            request,
            "products/category_form.html",
            {"form": CategoryForm(instance=category), "title": "Modifier la categorie", "category": category},
        )

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Categorie modifiee avec succes.")
            return redirect("category_list")
        return render(
            request,
            "products/category_form.html",
            {"form": form, "title": "Modifier la categorie", "category": category},
        )


class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, "products/category_confirm_delete.html", {"category": category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, "Categorie supprimee avec succes.")
        return redirect("category_list")
