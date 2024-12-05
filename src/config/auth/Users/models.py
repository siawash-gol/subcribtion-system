from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have username')
        if email is None:
            raise TypeError('Users must have email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password must not be None')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {
    'facebook': 'facebook', 'google': 'google', 'email': 'email'
}


class User(AbstractBaseUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
        admin = 'admin', 'Admin'
        student = 'student', 'Student'
        teacher = 'teacher', 'Teacher'

    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(_('email address'), unique=True)
    verified_email = models.BooleanField(default=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),

        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    role = models.CharField(
        _('role'),
        max_length=32,
        choices=RoleChoices.choices,
        default=RoleChoices.student
    )
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False,
        default=AUTH_PROVIDERS.get('email')
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        )
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site.")
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        if self.is_superuser:
            self.role = User.RoleChoices.admin
        super(User, self).save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
