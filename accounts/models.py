# Django imports
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from setup.basemodel import TimeBaseModel
import uuid


class MyAccountManager(BaseUserManager):
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError("Users must have an email address.")
		if "@" not in email and ".com" not in email:
			raise ValueError("Invalid email input")
		if len(password) < 8:
			raise ValueError("Password 8 must contain at least 8 characters")

		user = self.model(email=self.normalize_email(email))
		user.is_superuser = True
		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password):
		if not email:
			raise ValueError("Users must have an email address.")
		if "@" not in email and ".com" not in email:
			raise ValueError("Invalid email input")
		if len(password) < 8:
			raise ValueError("Password 8 must contain at least 8 characters")

		user = self.model(email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(max_length=200, blank=True, null=True)
	email = models.EmailField(unique=True, blank=True)
	balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	
	is_active = models.BooleanField(default=True)
	user_exist = models.BooleanField(default=False, null=True, blank=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last joined", auto_now=True)
	
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = MyAccountManager()

	USERNAME_FIELD = "email"
	# REQUIRED_FIELDS = [" "]

	class Meta:
		verbose_name_plural = "Users"
		ordering = ["-id"]

	def __str__(self):
		return self.email

	
	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Verification(TimeBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)

    def mark_as_expired_if_needed(self):
        # Calculate the time difference between now and when the code was sent
        time_difference = timezone.now() - self.sent_at

        # If more than one minute has passed, mark as expired
        if time_difference.total_seconds() >= 60:
            self.is_expired = True
            self.save()
