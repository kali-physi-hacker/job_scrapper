from django.contrib import admin
from .models import Profile, Document, CredentialVault


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "headline", "created_at")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("owner", "kind", "title", "ats_score", "created_at")


@admin.register(CredentialVault)
class CredentialVaultAdmin(admin.ModelAdmin):
    list_display = ("owner", "portal", "username", "created_at")

