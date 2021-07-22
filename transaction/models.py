from django.db import models
from datetime import datetime


# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)


class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)


class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)


# Create your models here.
def get_transaction_id():
    """
    this function gets latest count and returns new field
    :return: transaction_num
    """
    last_transaction = Transaction.objects.all().last()
    if not last_transaction:
        return "TRN/{}/{}".format(1,datetime.now().year)
    else:
        tran_num = last_transaction.transaction_number.split("/")[1]
        tran_year = last_transaction.transaction_number.split("/")[-1]
        if datetime.now().year > int(tran_year):
            return "TRN/{}/{}".format(1,datetime.now().year)
        else:
            return "TRN/{}/{}".format(int(tran_num)+1,tran_year)


class Transaction(models.Model):
    trans_choices = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('CLOSE', 'CLOSE')
    )
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=255,unique=True, default=get_transaction_id)
    transaction_status = models.CharField(max_length=9, choices=trans_choices)
    remarks = models.CharField(max_length=255, blank=True)


class LineItem(models.Model):
    unit_choices = (
        ('KG', 'KG'),
        ('METRE', 'METRE')
    )
    article = models.ForeignKey(ArticleMaster, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorMaster, on_delete=models.CASCADE)
    required_on_date = models.DateTimeField()
    quantity = models.FloatField()
    rate_per_unit = models.IntegerField()
    unit = models.CharField(max_length=5, choices=unit_choices)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)


class InventoryItem(models.Model):
    unit_choices = (
        ('KG', 'KG'),
        ('METRE', 'METRE')
    )
    article = models.ForeignKey(ArticleMaster, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorMaster, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.CASCADE)
    gross_quantity = models.DecimalField(max_digits=20, decimal_places=10)
    net_quantity = models.DecimalField(max_digits=20, decimal_places=10)
    unit = models.CharField(max_length=5, choices=unit_choices)
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
