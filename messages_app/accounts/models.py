import shortuuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import EmailField, BooleanField, DateTimeField, CharField
from django.contrib.auth.hashers import make_password, identify_hasher
from django.utils import timezone

from protus.auth.tokens import ProtusAuthTokenizer


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password, is_active=True, is_staff=False):
        if not email:
            raise ValueError('Укажите email')
        if not username:
            raise ValueError('Укажите имя')
        if not password:
            raise ValueError('Задайте пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.save(using=self._db)
        return user

    def create_oauth_user(self, email, username, uuid, is_active=True, is_verified=True, oauth_verified=True):
        """
        Метод для успешной интеграции с PROTUS-CLI - обязательные параметры email, username, uuid, oauth_verified.
        Остальные поля клиент настраивает под свою модель User
        """
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, uuid=uuid)
        user.is_active = is_active
        user.is_verified = is_verified
        user.oauth_verified = oauth_verified
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        if password is None:
            raise ValueError('Задайте пароль!')
        user = self.create_user(email, username, password=password, is_staff=True)
        return user


class User(AbstractBaseUser):
    email = EmailField(max_length=255, unique=True)
    username = CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_verified = BooleanField(default=True)  # in production change to True via email verification & for PROTUS users
    created_at = DateTimeField(default=timezone.now)
    uuid = CharField(max_length=50, null=True, blank=True)  # PROTUS specific field
    oauth_verified = BooleanField(default=False)  # PROTUS specific field

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def tokens(self):
        tokenizer = ProtusAuthTokenizer(self)
        refresh = tokenizer.tokenize_user()
        return {
            'refresh': str(refresh.token),
            'access': str(refresh.access_token.token),
        }

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.oauth_verified:
            try:
                _alg = identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
