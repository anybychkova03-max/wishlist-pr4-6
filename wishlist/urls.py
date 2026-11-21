from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("wishlist/", views.wishlist_list, name="wishlist_list"),
    path("wishlist/add/", views.add_wishlist_item, name="add_item"),
    path("wishlist/edit/<int:item_id>/", views.edit_wishlist_item, name="edit_item"),
    path("wishlist/delete/<int:item_id>/", views.delete_wishlist_item, name="delete_item"),
    path("wishlist/bought/<int:item_id>/", views.mark_item_bought, name="mark_bought"),
    path("purchased/return/<int:item_id>/", views.return_item_to_wishlist, name="return_item"),
    path("purchased/", views.purchased_list, name="purchased_list"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/edit/<int:category_id>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:category_id>/", views.delete_category, name="delete_category"),
]
