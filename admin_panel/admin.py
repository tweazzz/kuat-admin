from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    MainPage,
    Footer,
    PartnersSection,
    Partner,
    Request,
    Product,
    ProductCategory,
)

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("id",)


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("contact_title", "contact_email", "address_title", "location_title")
    search_fields = ("contact_title", "contact_email", "address_title", "location_title")


class PartnerInline(admin.TabularInline):
    model = Partner
    extra = 1


@admin.register(PartnersSection)
class PartnersSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    search_fields = ("title", "subtitle")
    inlines = [PartnerInline]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "url")
    search_fields = ("name", "url")
    list_filter = ("section",)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company", "email", "phone", "is_processed", "created_at")
    list_filter = ("is_processed", "created_at")
    search_fields = ("first_name", "last_name", "company", "email", "phone")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "description", "category__name")
    list_filter = ("category",)