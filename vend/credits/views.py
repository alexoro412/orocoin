import datetime
import subprocess
import uuid
import os

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import credits.models
from credits.forms import UserProfileForm, UserForm, SpendForm, StlForm, transForm, SubmissionForm, JobForm, AcceptForm
from credits.models import PendingTransactions, Purchase, Design, Job, Submission, AddTransaction


email_address = settings.EMAIL_HOST_USER

# TODO add job monitoring interface
# Needs --
# ! Remove job (liquidates money)
#   Accept submission (pays out)
#   Model previews?

# TODO make submission accept Design model, not STL

# TODO prompt deletion of models and jobs

# TODO make sure negative costs are not accepted anywhere

# TODO implement color preference change

# TODO make descriptions wrap

@login_required
def delete_job(request):
    print "here"
    if request.method == 'POST':
        print "here"
        job_id = request.POST.get('name')
        job = Job.objects.get(name=job_id)
        if job.owner == request.user:
            job.owner.profile.credits += job.cost
            job.owner.profile.save()
            job.delete()
            return HttpResponse('Deleted')
        return HttpResponse('Please report this error to alex: error number ab5')
    return HttpResponseRedirect('/credits/')


@login_required
def monitor_job(request):
    job_id = request.GET.get('id')
    job = Job.objects.get(name=job_id)
    subms = Submission.objects.all().filter(job=job)
    if not job.owner == request.user:
        return HttpResponseRedirect('/credits/')
    return render(request, 'job_monitor.html', {'job': job, 'subms': subms})

@login_required
def delete_design(request):
    print 'he'
    if request.method == 'POST':
        print 'here'
        model_id = request.POST.get('name')
        print request.POST
        model = Design.objects.get(name=model_id)
        model.delete()
        return HttpResponse('deleted model')
    print 'oop'
    return HttpResponseRedirect('/credits/')

@login_required
def index(request):
    trans = PendingTransactions.objects.all().filter(purchaser=request.user)
    translen = []
    items = Purchase.objects.all()
    itemlen = []
    for item in items:
        itemlen.append([item, len(trans.filter(purchased=item))])
    stl = request.GET.get('s', '')
    stl_failed = False
    if stl == 'f':
        stl_failed = True
    purchases = []
    designs = Design.objects.all().filter(owner=request.user)
    for purch in trans:
        if purch.purchased not in purchases:
            purchases.append(purch.purchased)
    context = {'trans': trans, 'items': itemlen, 'purchases': purchases, 'designs': designs, 'translen': translen, 'stl_failed': stl}
    return render(request, 'index.html', context)


@login_required
def purchase_list(request):
    trans = PendingTransactions.objects.all().filter(purchaser=request.user).filter(processed=False)
    translen = []
    items = Purchase.objects.all()
    itemlen = []
    for item in items:
        itemlen.append([item, len(trans.filter(purchased=item))])
    purchases = []
    designs = Design.objects.all().filter(owner=request.user)
    for purch in trans:
        if purch.purchased not in purchases:
            purchases.append(purch.purchased)
    context = {'trans': trans, 'items': itemlen, 'purchases': purchases, 'designs': designs, 'translen': translen}
    return render(request, 'purchaselist.html', context)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/credits/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/credits/')


"""
Arbitrary code can be executed here, like:
1. Sending data to the vending machine to dispense shtuff
2. Sending an email to someone
3. Anything you can do in python
The processed/redeemed variable of an object can be modified at this point
for example, if the vending machine is down, the purchases can remain un redeemed
layout: separate .py file for spending functions
i.e. socket connection to arduino, email to person
"""


@login_required
def spend(request):
    if request.method == 'POST':
        form = SpendForm(request.POST)
        print form.data
        if form.data['name']:
            purch = Purchase.objects.get(pk=form.data['name'])
            spent = request.user.profile.spend(purch.amount)
            t = AddTransaction(purch, request.user, spent)
        else:
            print 'A purchase failed'
            return HttpResponse('critical error. name not in form')
        if spent:
            return HttpResponse('You purchased ' + Purchase.objects.get(pk=form.data['name']).name + '!!!!')
    else:
        return render(request, 'buy.html', {'form': SpendForm, 'money': True})


@login_required
def redeem(request):
    trans_id = request.GET.get('c', '')
    trans = PendingTransactions.objects.get(identifier=trans_id)
    # The same spend code can be executed here as well
    trans.processed = True
    trans.save()
    return HttpResponseRedirect('/credits/')


@login_required
def order(request):
    design_id = request.GET.get('item', '')
    design = Design.objects.get(name=design_id)
    spent = request.user.profile.spend(design.cost)
    if spent:
        send_mail(
            'Ordered model - ' + design.title + ' - ' + design.owner.username + ' - ' + str(datetime.datetime.now()),
            design.owner.username + ' just order http://127.0.0.1:8000' + design.stl.url + ' so print it! code: ' + design.name + ' (hunter, if you\'re reading this, that link won\'t work, don\'t try it. it will work once I fully set up the credits site at oro.kentdenver.org)',
            email_address, ['3d@kentdenver.org'])
        return HttpResponse('Model ordered succesfully')
    return HttpResponse('Could not order model -- Not enough money')


@login_required
def upload(request):
    if request.method == 'POST':
        stlform = StlForm(request.POST, request.FILES)
        if stlform.is_valid():
            stl = stlform.save(commit=False)
            stl.owner = request.user
            stl.name = uuid.uuid4()
            stl.save()
            costBack = stlCost(stl)
            if costBack[0] == -1 or costBack[1] == -1 or costBack[2] == -1:
                stl.delete()
                return HttpResponseRedirect('/credits/?s=f')
            stl.cost = costBack[0]
            stl.volume = costBack[1]
            stl.area = costBack[2]
            stl.save()
            return HttpResponseRedirect('/credits/')
        else:
            print stlform.errors
    else:
        stlform = StlForm()
    return render(request, 'upload.html', {'stlform': stlform})


@login_required
def transfer(request):
    daform = transForm()
    if request.method == 'POST':
        daform = transForm(request.POST)
        da = daform.save(commit=False)
        spent = request.user.profile.spend(da.cost)
        if spent:
            rec = da.recipient.profile
            rec.credits += da.cost
            rec.save()
            send_mail('Transferred funds',
                      'you just received money from ' + request.user.username + ' . How kind of them. they gave you ' + str(
                          da.cost) + ' Orocoins. yay!!!!!!!!!!', email_address, [da.recipient.email])
            return HttpResponseRedirect('/credits/')
        else:
            return HttpResponse('Failed to transfer funds')
    else:
        daform = transForm()
    return render(request, 'transfer.html', {'daform': daform})


# @login_required
# def delete_design(request):
#     design_id = request.GET.get('item', '')
#     design = Design.objects.get(name=design_id)
#     if design.owner == request.user:
#         design.delete()
#     return HttpResponseRedirect('/credits/')


@login_required
def new_job(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        fo = form.save(commit=False)
        fo.owner = request.user
        fo.name = uuid.uuid4()
        spent = fo.owner.profile.spend(fo.cost)
        if spent:
            fo.save()
        else:
            return render(request, 'new_job.html', {'form': form, 'money': False})
        return HttpResponseRedirect('/credits/')
    else:
        form = JobForm()
    return render(request, 'new_job.html', {'form': form, 'money': True})


@login_required
def new_submission(request):
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        fo = form.save(commit=False)
        fo.submitter = request.user
        fo.name = uuid.uuid4()
        fo.save()
        return HttpResponseRedirect('/credits/')
    else:
        job_id = request.GET.get('job', '')
        form = SubmissionForm()
        job = Job.objects.get(name=job_id)
    form.fields['job'].initial = Job.objects.get(name=job_id)
    return render(request, 'new_submission.html', {'form': form, 'job': job})


# @login_required
# def delete_job(request):
#     job_id = request.GET.get('job', '')
#     job = Job.objects.get(name=job_id)
#     if request.user == job.owner:
#         request.user.profile.credits += job.cost
#         request.user.profile.save()
#         job.delete()
#     return HttpResponseRedirect('/credits/')


@login_required
def accept_submission(request):
    if request.method == 'POST':
        form = AcceptForm(request.POST)
        fo = form.save(commit=False)

    # else:
    #     job_id = request.GET.get('job', '')
    #     subm_id = request.GET.get('subm', '')
    #     form = AcceptForm()
    #     # form.fields['job'].initial = Job.objects.get(name=job_id)
    #     # form.fields['submission'].initial = Submission.objects.get(name=subm_id)
    #     fo = form.save(commit=False)
    #     # fo.job = Job.objects.get(name=job_id)
    #     fo.submission = Submission.objects.get(name=subm_id)
    #     fo.job = fo.submission.job
    #     # fo.save()
    #     fo.submission.submitter.profile.credits += fo.job.cost
    #     fo.submission.submitter.profile.save()
    #     # fo.job.delete()
    return HttpResponseRedirect('/credits/')

@login_required
def models_3d(request):
    designs = Design.objects.all().filter(owner=request.user)
    return render(request, '3dmodels.html', {'designs': designs})

@login_required
def job_list(request):
    jobs = Job.objects.all().filter(archived=False)
    return render(request, 'jobs.html', {'jobs': jobs})

@login_required
def wallet(request):
    return HttpResponse(request.user.profile.credits)


#########################
#                       #
# STL Cost Calculations #
#                       #
#########################

def stlCost(stl):
    admesh_output = subprocess.Popen([os.path.join(settings.BASE_DIR, "credits", "vol"), stl.stl.path],stdout=subprocess.PIPE).communicate()[0]
    volume = float(admesh_output.split()[7])
    surface_area = parseSTL(stl.stl.path)
    if surface_area == -1:
        return [-1,-1,-1]
    cost = (((surface_area) * 2 + ((volume / 100) * 10)) * .253) / 62.5748637
    return [cost,volume,surface_area]

#################################
#                               #
# STL Surface Area calculations #
#                               #
#################################

def calcArea(p1,p2,p3):
	m11 = 1
	m12 = 1
	m13 = 1

	m21 = p2[0]-p1[0]
	m22 = p2[1]-p1[1]
	m23 = p2[2]-p1[2]
	m31 = p3[0]-p1[0]
	m32 = p3[1]-p1[1]
	m33 = p3[2]-p1[2]

	a = m31*m22*m13
	b = m32*m23*m11
	c = m33*m21*m12
	d = m11*m22*m33
	e = m12*m23*m31
	f = m13*m21*m32

	return abs(0.5*(a+b+c-d-e-f))


def parseSTL(filename):
	f = open(filename)
	content = f.readlines()
	vertexes = []
	line1 = content[0].split()
	if not line1[0] == "solid":
		return -1
	for i in range(0,len(content)):
		line = content[i].split()
		if line[0] == 'vertex':
			vertexes.append(content[i])
	sum = 0
	for i in range(0,len(vertexes),3):
		line = vertexes[i].split()
		l1 = parseLine(vertexes[i].split())
		l2 = parseLine(vertexes[i+1].split())
		l3 = parseLine(vertexes[i+2].split())
		sum += calcArea(l1,l2,l3)
	f.close()
	return sum


def parseLine(line):
	if line[0] == 'vertex':
		return [float(line[1]),float(line[2]),float(line[3])]
