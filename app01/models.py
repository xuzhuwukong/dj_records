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
