from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import CheckoutForm
from .models import Order, OrderItem
from products.models import Product

SHIPPING_FEE = Decimal("30.00")


def _get_cart(request):
    return request.session.setdefault("cart", {})


def _cart_items(request):
    cart = _get_cart(request)
    items = []
    subtotal = Decimal("0.00")

    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            continue
        quantity = int(quantity)
        line_total = product.price * quantity
        subtotal += line_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            }
        )
    total = subtotal + SHIPPING_FEE if items else Decimal("0.00")
    return items, subtotal, total


class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = _get_cart(request)
        cart[str(product.pk)] = int(cart.get(str(product.pk), 0)) + 1
        request.session.modified = True
        messages.success(request, f"{product.name} ajoute au panier.")
        return redirect("cart_detail")


class CartDetailView(View):
    def get(self, request):
        items, subtotal, total = _cart_items(request)
        return render(
            request,
            "orders/cart_detail.html",
            {"items": items, "subtotal": subtotal, "shipping_fee": SHIPPING_FEE if items else 0, "total": total},
        )


class UpdateCartItemView(View):
    def post(self, request, pk):
        cart = _get_cart(request)
        quantity = max(1, int(request.POST.get("quantity", 1)))
        cart[str(pk)] = quantity
        request.session.modified = True
        return redirect("cart_detail")


class RemoveCartItemView(View):
    def post(self, request, pk):
        cart = _get_cart(request)
        cart.pop(str(pk), None)
        request.session.modified = True
        messages.success(request, "Produit retire du panier.")
        return redirect("cart_detail")


class CheckoutView(View):
    def get(self, request):
        items, subtotal, total = _cart_items(request)
        form = CheckoutForm()
        return render(
            request,
            "orders/checkout.html",
            {
                "form": form,
                "items": items,
                "subtotal": subtotal,
                "shipping_fee": SHIPPING_FEE if items else 0,
                "total": total,
            },
        )

    def post(self, request):
        items, subtotal, total = _cart_items(request)
        form = CheckoutForm(request.POST)
        if not items:
            messages.error(request, "Le panier est vide.")
            return redirect("product_list")
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data["customer_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                shipping_fee=SHIPPING_FEE,
                subtotal=subtotal,
                total=total,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    unit_price=item["product"].price,
                    line_total=item["line_total"],
                )
            request.session["cart"] = {}
            messages.success(request, "Commande creee avec succes.")
            return redirect("checkout_success", pk=order.pk)
        return render(
            request,
            "orders/checkout.html",
            {
                "form": form,
                "items": items,
                "subtotal": subtotal,
                "shipping_fee": SHIPPING_FEE if items else 0,
                "total": total,
            },
        )


class CheckoutSuccessView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk)
        return render(request, "orders/checkout_success.html", {"order": order})
