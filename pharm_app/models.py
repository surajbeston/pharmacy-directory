from django.db import models

class pharma(models.Model):
    organization_name = models.CharField(max_length = 200)
    entry_id = models.CharField(max_length = 200, blank = True)
    location_address_1 = models.CharField(max_length = 200)
    location_address_2 = models.CharField(max_length = 200, blank = True)
    email = models.CharField(max_length = 300)
    mobile = models.DecimalField(max_digits = 10, decimal_places = 0)
    password = models.CharField(max_length = 300)
    authentication_file = models.CharField(max_length = 206, blank = True)
    activated = models.BooleanField(default = False)
    encryption_key = models.CharField(max_length = 200)
    datetime = models.DateTimeField(auto_now_add = True)

class signin_info(models.Model):
    pharmaceutical = models.ForeignKey(pharma, on_delete = models.CASCADE)
    signin_datetime = models.DateTimeField(auto_now_add = True)
    signout_datetime = models.DateTimeField(blank = True)

class activation_info(models.Model):
    pharmaceutical = models.ForeignKey(pharma, on_delete = models.CASCADE)
    activation_datetime = models.DateTimeField(auto_now_add = True)
    pin = models.DecimalField(max_digits=6, decimal_places = 0)
    link_randcode = models.CharField(max_length = 50)

class download_record(models.Model):
    key = models.CharField(max_length = 100)
    filename = models.CharField(max_length = 206)
    file_path = models.CharField(max_length = 228)
    created_datetime = models.DateTimeField(auto_now_add = True)
    expiry_datetime = models.DateTimeField(blank = True)
    downloaded = models.BooleanField(default = False)

class medicine_info(models.Model):
    identification = models.CharField(max_length = 200)
    medicine = models.CharField(max_length = 300)
    info = models.CharField(max_length = 500)
    added_composition = models.BooleanField(default = False)
    added_datetime = models.DateTimeField(auto_now_add = True)

class medicine_composition(models.Model):
    medicine = models.ForeignKey(medicine_info, on_delete = models.CASCADE)
    composition = models.CharField(max_length = 300)
    weightage = models.DecimalField(max_digits = 8, decimal_places = 4)

class keys_key(models.Model):
    key = models.CharField(max_length = 100)
    token = models.CharField(max_length = 100)
