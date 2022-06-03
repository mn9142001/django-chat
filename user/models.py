from django.db import models
from django.contrib.auth.models import AbstractUser


def get_profile_pic_path(instance, filename):
	return 'profiles/{0}/pic/{1}'.format(instance.email, filename)

class User(AbstractUser):

	avatar = models.ImageField(upload_to=get_profile_pic_path, null=True, blank=True,)
	chatted_with = models.ManyToManyField('self', blank=True)
	stranger_chats = models.ManyToManyField('self', blank=True)

	@property
	def cover(self):
		if not self.avatar:
			return '/media/images/profiles/user-profile.png'
		return self.avatar

	@property
	def name(self):
		if not self.first_name:
			return self.username
		return self.first_name.capitalize() + " " + self.last_name.capitalize()

	def get_first_name(self):
		if not self.first_name:
			return self.name()
		return self.first_name.capitalize()

	def __str__(self):
		return str(self.id) + ": " + self.name()
