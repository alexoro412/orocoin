from django.contrib import admin
from credits.models import UserProfile, Purchase, PendingTransactions, Design, Job, Submission
from credits.models import Accept
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Purchase)
admin.site.register(PendingTransactions)
admin.site.register(Design)
admin.site.register(Job)
admin.site.register(Submission)
admin.site.register(Accept)
