
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name


class WishlistItem(models.Model):
    PRIORITY_CHOICES = [
        ("high", "Высокий"),
        ("medium", "Средний"),
        ("low", "Низкий"),
    ]

    STATUS_CHOICES = [
        ("want", "Хочу приобрести"),
        ("bought", "Куплено"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория"
    )
    title = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость"
    )
    url = models.URLField(blank=True, verbose_name="Ссылка на товар")
    image = models.ImageField(
        upload_to="wishlist/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
        verbose_name="Приоритет"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="want",
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    def __str__(self):
        return self.title


class Purchase(models.Model):
    item = models.OneToOneField(
        WishlistItem,
        on_delete=models.CASCADE,
        related_name="purchase",
        verbose_name="Товар"
    )
    purchase_date = models.DateField(verbose_name="Дата покупки")
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Фактическая стоимость"
    )

    def __str__(self):
        return f"Покупка: {self.item.title}"

