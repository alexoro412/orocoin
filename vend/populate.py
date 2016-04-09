
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vend.settings')

import django
django.setup()

from credits.models import Purchase, Job, Submission, UserProfile
from django.contrib.auth.models import User
import uuid

def add_user(username, theme):
	user = User(username=username)
	user.set_password('password')
	user.save()
	user_profile = UserProfile(user=user, credits=100, color=theme)
	user_profile.save()

add_user('foo', 'blue-grey')
add_user('bar', 'cyan')

#Jobs # create a test job for another user, and for the example user
def add_job(title, desc, name, username, cost):
	j = Job(name=name)#Job.objects.get_or_create(name=name)[0]
	j.title = title
	j.desc = desc
	j.owner = User.objects.get(username=username)
	j.save()

add_job('Make a wizard', 'I want a 3D model of a wizard', uuid.uuid4(), 'foo', 10)
add_job('Make a planet', 'I want a kewl low poly planet', uuid.uuid4(), 'bar', 4)
#Purchase # items that can be purchased
def add_item(name, amount, desc):
	i = Purchase(name=name, amount=amount, desc=desc)
	i.save()

add_item('Snack Bar', 1, 'one bar of snack')
add_item('Food piece', 2, 'one piece of food')
