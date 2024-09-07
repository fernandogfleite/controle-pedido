from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models

from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, Base):

    email = models.EmailField(_("Email Address"), unique=True, max_length=255)
    name = models.CharField(_("Name"), max_length=255)

    clients = models.ManyToManyField(
        "Client", through="ClientUser", related_name="users"
    )

    is_active = models.BooleanField(_("Active"), default=True)
    is_confirmed = models.BooleanField(_("Confirmed"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "is_confirmed"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users"

    def __str__(self):
        return self.name


class Client(Base):
    CPF = "CPF"
    CNPJ = "CNPJ"

    DOCUMENT_TYPE_CHOICES = (
        (CPF, "CPF"),
        (CNPJ, "CNPJ"),
    )

    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    document_type = models.CharField(
        _("Document Type"), max_length=4, choices=DOCUMENT_TYPE_CHOICES
    )
    document_number = models.CharField(_("Document Number"), max_length=14)
    phone = models.CharField(_("Phone Number"), max_length=15)
    address = models.TextField(_("Address"))

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        db_table = "clients"

    def __str__(self):
        return self.name


class ClientUser(Base):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_users"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="client_users"
    )

    class Meta:
        verbose_name = _("Client User")
        verbose_name_plural = _("Client Users")
        db_table = "client_users"

    def __str__(self):
        return f"{self.client.name} - {self.user.name}"
