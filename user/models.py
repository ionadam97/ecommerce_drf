from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core.models import TimeStampedModel


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return "uploads/users/{0}/{1}".format(instance.user.username, filename)


class ShippingAddress(TimeStampedModel):
	user = models.ForeignKey(get_user_model(), related_name='address', on_delete=models.CASCADE)
	country = CountryField(blank=False, null=False)
	phone_number = PhoneNumberField(null=True, blank=True)
	city = models.CharField(max_length=200)
	zipcode = models.CharField(max_length=200)
	street = models.CharField(max_length=200)

	def __str__(self):
		return self.user.username


class Profile(TimeStampedModel):

	GENDER_MALE = "m"
	GENDER_FEMALE = "f"
	OTHER = "o"
	GENDER_CHOICES = (
		(GENDER_MALE, "Male"),
		(GENDER_FEMALE, "Female"),
		(OTHER, "Other"),
	)

	user = models.OneToOneField(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	phone_number = PhoneNumberField(null=True, blank=True)
	image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
	birth_date = models.DateField(blank=True, null=True)
	

	class Meta:
		ordering = ['-created']
	
	def __str__(self):
		return self.user.username

    
