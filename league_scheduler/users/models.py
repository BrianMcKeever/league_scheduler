from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, discord_id, discord_name, discord_discriminator, **extra_fields):
        """
        Create and save a User with the provided info
        """
        if not discord_name:
            raise ValueError("The given discord_name must be set")
        if not discord_discriminator:
            raise ValueError("The given discord_discriminator must be set")
        if not discord_id:
            raise ValueError("The given discord_id must be set")

        user = self.model(discord_name=discord_name, discord_id = discord_id,
                discord_discriminator=discord_discriminator, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, discord_id, discord_name, discord_discriminator, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(discord_id, discord_name, discord_discriminator, **extra_fields)

    def create_superuser(self, discord_id, discord_name, discord_discriminator, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(discord_id, discord_name, discord_discriminator, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    MyUser model that uses discordid instead of usernames

    All other fields from the Django auth.User model are kept to
    ensure compatibility with the built in management commands.
    """

    discord_id = models.CharField(max_length=32, unique=True) #I can't find how long these can be. My snowflake id is 18 numbers
    discord_name = models.CharField(max_length=32)
    discord_discriminator = models.CharField(max_length=4)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "discord_id"
    REQUIRED_FIELDS = [discord_id, discord_discriminator, discord_name]

    class Meta:
        verbose_name = "MyUser"
        verbose_name_plural = "MyUsers"

    def get_full_name(self):
        return "%s#%s"%(self.discord_name, self.discord_id)

    def get_short_name(self):
        return self.discord_name
