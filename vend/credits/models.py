from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid
# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile")
	credits = models.IntegerField(default=0)
	color = models.CharField(max_length=40,default="blue-grey")
	def __unicode__(self):
		return self.user.username
	def spend(self, amount):
		spent = False
		if self.can_spend_amount(amount) and amount > 0:
			self.credits = self.credits - amount
			spent = True
		self.save()
		return spent
	def can_spend(self):
		return self.credits > 0
	def can_spend_amount(self, amount):
		return self.credits >= amount


class Purchase(models.Model):
	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True)
	amount = models.IntegerField(default=0)
	desc = models.CharField(max_length=140)
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Purchase, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.name + '  $' + str(self.amount)


class PendingTransactions(models.Model):
	purchased = models.ForeignKey(Purchase)
	purchaser = models.ForeignKey(User, related_name="purchases")
	processed = models.BooleanField(default=False)
	identifier = models.CharField(default=uuid.uuid4,unique=True,blank=True,null=True,max_length=100)
	def __unicode__(self):
		return self.purchaser.__unicode__() + ' - ' + self.purchased.__unicode__() + ' - ' + self.identifier


def AddTransaction(purchased, purchaser, spent, processed=False,name="name"):
	#print "here also"
	#print purchaser.profile.can_spend_amount(purchased.amount)
	#print purchased.amount
	if spent:
		p = PendingTransactions.objects.create(purchased=purchased,purchaser=purchaser,processed=False)
		p.save()
		#print "here"
		#print p
                return p
	return 0


class Design(models.Model):
	title = models.CharField(max_length=100)
	name = models.CharField(unique=True,max_length=100)
	desc = models.CharField(max_length=140)
	stl = models.FileField(upload_to='stl')
	owner = models.ForeignKey(User)
	cost = models.IntegerField(default=0)
	area = models.IntegerField(default=0)
	volume = models.IntegerField(default=0)
	def __unicode__(self):
		return self.name + ' - ' + self.owner.__unicode__()


class Transfer(models.Model):
	cost = models.IntegerField(default=0)
        recipient = models.ForeignKey(User)


class Job(models.Model):
	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=1000)
	name = models.CharField(max_length=100,unique=True) #uuid4
	owner = models.ForeignKey(User)
	cost = models.IntegerField(default=0)
	archived = models.BooleanField(default=False)
        def __unicode__(self):
		return self.title + ' - ' + self.owner.username


class Submission(models.Model):
	submitter = models.ForeignKey(User)
	job = models.ForeignKey(Job)
	submission = models.FileField(upload_to='stl')
	name = models.CharField(max_length=100) #uuid4
	def __unicode__(self):
		return self.job.title + ' - ' + self.submitter.__unicode__()


class Accept(models.Model):
	job = models.ForeignKey(Job)
	submission = models.ForeignKey(Submission)
	def __unicode__(self):
		return self.job.title + ' : ' + self.submission.submitter.__unicode__() + ' -> ' + self.job.owner.__unicode__()
