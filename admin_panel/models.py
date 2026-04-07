from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.EDITOR)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.SUPER_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        EDITOR = "editor", "Editor"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EDITOR,
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class MainPage(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    background_image = models.ImageField(upload_to='main_page/')

    def __str__(self):
        return "Main Page"
    


from django.db import models


class Footer(models.Model):
    contact_title = models.CharField(max_length=100, default="Contact Us")
    contact_phones = models.JSONField(default=list, blank=True)
    contact_email = models.EmailField()

    address_title = models.CharField(max_length=100, default="Address")
    address = models.TextField()

    location_title = models.CharField(max_length=100, default="Location")
    map_url = models.URLField()

    copyright_text = models.CharField(
        max_length=255,
        default="© 2026 Kuat. All rights reserved."
    )

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def save(self, *args, **kwargs):
        # singleton: always keep only one footer row
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Footer"


class PartnersSection(models.Model):
    title = models.CharField(max_length=120, default="Our partners")
    subtitle = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Partners section"
        verbose_name_plural = "Partners section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Partners section"


class Partner(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField()
    logo = models.ImageField(upload_to="partners/")

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name
    



class Request(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company})"
    


class ProductCategory(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name