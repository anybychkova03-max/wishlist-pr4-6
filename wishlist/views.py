from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import WishlistItem, Category

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            default_categories = Category.objects.filter(user__isnull=True)
            for category in default_categories:
                Category.objects.create(user=user, name=category.name, description=category.description)
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "wishlist/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "wishlist/login.html", {"form": form})


@login_required(login_url="login")
@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect("home")

def home(request):
    if request.user.is_authenticated:
        items = WishlistItem.objects.filter(user=request.user)
    else:
        items = WishlistItem.objects.none()

    return render(request, "wishlist/home.html", {
        "total_items": items.count(),
        "bought_items": items.filter(status="bought").count(),
        "categories_count": Category.objects.filter(user=request.user).count() if request.user.is_authenticated else 0,
        "recent_items": items.order_by("-created_at")[:3],
    })

@login_required(login_url="login")
def wishlist_list(request):
    items = WishlistItem.objects.filter(
        user=request.user,
        status="want"
    )
    return render(request, "wishlist/wishlist_list.html", {"items": items})


@login_required(login_url="login")
def purchased_list(request):
    items = WishlistItem.objects.select_related("category").filter(
        user=request.user,
        status="bought"
    ).order_by("-created_at")

    return render(request, "wishlist/purchased_list.html", {"items": items})

@login_required(login_url="login")
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "wishlist/category_list.html", {"categories": categories.order_by("name")})

@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        Category.objects.create(user=request.user, name=request.POST.get("name"), description=request.POST.get("description", ""))
        return redirect("category_list")
    return render(request, "wishlist/add_category.html")

@login_required(login_url="login")
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.description = request.POST.get("description", "")
        category.save()
        return redirect("category_list")
    return render(request, "wishlist/edit_category.html", {"category": category})

@login_required(login_url="login")
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "wishlist/delete_category.html", {"category": category})

@login_required(login_url="login")
def add_wishlist_item(request):
    categories = Category.objects.all()
    if request.method == "POST":
        WishlistItem.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            price=request.POST.get("price"),
            url=request.POST.get("url", ""),
            image=request.FILES.get("image"),
            category_id=request.POST.get("category") or None,
            priority=request.POST.get("priority", "medium"),
            status="want",
        )
        return redirect("wishlist_list")
    return render(request, "wishlist/add_item.html", {"categories": categories})

@login_required(login_url="login")
def edit_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    categories = Category.objects.all()
    if request.method == "POST":
        item.title = request.POST.get("title")
        item.description = request.POST.get("description", "")
        item.price = request.POST.get("price")
        item.url = request.POST.get("url", "")
        item.category_id = request.POST.get("category") or None
        item.priority = request.POST.get("priority", "medium")
        uploaded_image = request.FILES.get("image")
        if uploaded_image:
            item.image = uploaded_image
        item.save()
        return redirect("wishlist_list")
    return render(request, "wishlist/edit_item.html", {
        "item": item,
        "categories": categories,
    })

@login_required(login_url="login")
def delete_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("wishlist_list")
    return render(request, "wishlist/delete_item.html", {"item": item})

@login_required(login_url="login")
def mark_item_bought(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
        item.status = "bought"
        item.save()

    return redirect("wishlist_list")

@login_required(login_url="login")    
def return_item_to_wishlist(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
        item.status = "want"
        item.save()

    return redirect("purchased_list")