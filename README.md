# orocoin
An online marketplace tied closely to Kent Denver's 3D printer (and fictitious vending machine)

### Powered by Django 1.7, Bootstrap, and Material Designs

---
## setting up

edit the file settings.py at vend/vend/settings.py
```python
#line 88:
EMAIL_HOST_USER: #set a user for an email account
#line 89:
EMAIL_HOST_PASSWORD: #set the password the email account
```

it may be necessary to edit other email settings(which are defined in nearby lines) if the email account used is not a gmail account

orocoin will use this email account to notify people of receiving funds, receipts for prints, notify the printer's email account of a new print, etc...

then run
```
cd vend
python manage.py migrate # to initialise the database
python populate.py # to create some example users, jobs, and products
```

---
## running
```
python manage.py runserver
```
now goto localhost:8000/credits

the existing users are foo and bar. Their passwords are both password

Using the nav bar upload a 3d model (it currently must be an stl in ascii format. the project was stopped before better support for this and other features). in order for this to work, you must have [admesh](https://github.com/admesh/admesh) installed

---
## Features:
- Order items from an arduino powered vending machine (if it was ever made...)
- Post jobs, submit files to jobs, and review files
- Transfer funds
- upload 3d models, view volume, surface area, and cost to print
- order models to be printed


please note this entire system is set to email 3D@kentdenver.org for every print ordered, so if intending to test this server, it is recommended to change that. this was not made easy to change because it is never intended to email any other printers.
