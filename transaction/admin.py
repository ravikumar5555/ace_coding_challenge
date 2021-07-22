from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.LineItem)
admin.site.register(models.InventoryItem)
admin.site.register(models.ColorMaster)
admin.site.register(models.ArticleMaster)
admin.site.register(models.Transaction)
admin.site.register(models.DepartmentMaster)
admin.site.register(models.BranchMaster)
admin.site.register(models.CompanyLedgerMaster)
