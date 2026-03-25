from django.contrib import admin

from .models import MainPage, Footer, PartnersSection

@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("contact_title", "contact_email", "address_title", "location_title")

@admin.register(PartnersSection)
class PartnersSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)