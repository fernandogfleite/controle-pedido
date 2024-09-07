# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from api.apps.authentication.models.client import User, Client, ClientUser


class UserAdmin(BaseUserAdmin):
    # Definir os campos a serem exibidos na lista de usuários
    list_display = ("email", "name", "is_active", "is_confirmed", "is_staff")
    list_filter = ("is_active", "is_confirmed", "is_staff")

    # Campos exibidos ao visualizar/editar um usuário
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_confirmed",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )

    # Campos exibidos ao adicionar um novo usuário
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_confirmed",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    # Campos utilizados para busca
    search_fields = ("email", "name")

    # Definir qual campo utilizar para ordenar a lista de usuários
    ordering = ("email",)

    # Quantos usuários exibir por página
    list_per_page = 25

    # Definir o campo que será usado como identificador do usuário
    filter_horizontal = ("groups", "user_permissions", "clients")


class ClientAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de clientes
    list_display = ("name", "slug", "document_type", "document_number", "phone")
    list_filter = ("document_type",)

    # Campos exibidos ao visualizar/editar um cliente
    fieldsets = (
        (None, {"fields": ("name", "slug")}),
        (
            _("Details"),
            {"fields": ("document_type", "document_number", "phone", "address")},
        ),
    )

    # Campos utilizados para busca
    search_fields = ("name", "document_number", "phone")

    # Ordenação padrão
    ordering = ("name",)

    # Quantos clientes exibir por página
    list_per_page = 25


class ClientUserAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de ClientUsers
    list_display = ("client", "user")

    # Campos utilizados para busca
    search_fields = ("client__name", "user__name")

    # Filtros
    list_filter = ("client", "user")

    # Quantos ClientUsers exibir por página
    list_per_page = 25


# Registro do modelo ClientUser no admin
admin.site.register(ClientUser, ClientUserAdmin)
# Registro do modelo Client no admin
admin.site.register(Client, ClientAdmin)
# Registro do modelo User no admin
admin.site.register(User, UserAdmin)
