from django.contrib import admin

from .models import MainPage, Footer, PartnersSection, Request, Product, ProductCategory

@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("contact_title", "contact_email", "address_title", "location_title")

@admin.register(PartnersSection)
class PartnersSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)



@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company", "email", "is_processed", "created_at")
    list_filter = ("is_processed",)
    search_fields = ("first_name", "last_name", "company", "email")


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [ProductInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")