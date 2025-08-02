from django.db import models

class MisuseEntry(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zone = models.CharField(max_length=50)
    public_dc = models.CharField(max_length=50)
    bp_no = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)
    load_kw = models.CharField(max_length=50)
    meter_make = models.CharField(max_length=50)
    meter_sn = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    pulse = models.CharField(max_length=50)
    reading = models.CharField(max_length=50)
    md = models.CharField(max_length=50)
    ph = models.CharField(max_length=50)
    remark = models.TextField()
