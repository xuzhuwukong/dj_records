from django.db import models

# Create your models here.


class Record(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    publish_date = models.DateField()
    engineer = models.ForeignKey(to="Engineer", to_field="nid", on_delete=models.CASCADE)
    periods = models.ManyToManyField(to="Period")


class Engineer(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    addr = models.CharField(max_length=32)


class Period(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

class Order(models.Model):
    nid = models.AutoField(primary_key=True)
    po_name = models.CharField(max_length=12)
    open_date = models.DateField()
    case_number = models.CharField(max_length=8)
    account_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=12)
    serial_number = models.CharField(max_length=12)
    cost_type = models.CharField(max_length=12)
    internal_summary = models.CharField(max_length=200)
    promise_date = models.DateField()
    total_price = models.CharField(max_length=10) 
# Customer PO#	Date/Time Opened	Case Number	Account Name (Local)	Product Code	Serial Number	Cost Type	Internal Summary	Promise Date	Total Price (converted).amount