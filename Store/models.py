from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class Custom(AbstractUser):
    class Role(models.TextChoices): 
        SUPER_ADMIN = "SUPER_ADMIN", 'SUPER_ADMIN'
        ADMIN = "ADMIN", 'ADMIN'
        MANAGER = "MANAGER", 'MANAGER'
        GATE_MANAGER = "GATE_MANAGER", 'GATE_MANAGER'
    
    base_role = Role.SUPER_ADMIN
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)

    company_name = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            if self.role == self.Role.ADMIN:
                self.base_role = self.Role.ADMIN
            elif self.role == self.Role.MANAGER:
                self.base_role = self.Role.MANAGER
            elif self.role == self.Role.GATE_MANAGER:
                self.base_role = self.Role.GATE_MANAGER
        super().save(*args, **kwargs)
    
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN
    
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    def is_manager(self):
        return self.role == self.Role.MANAGER
    
    def is_gate_manager(self):
        return self.role == self.Role.GATE_MANAGER
    
class UserPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.permission}"   

class Company(models.Model):
    company_name = models.TextField(null=False, blank=False,unique=True)
    owner_firm_manager = models.TextField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    experience = models.FloatField(max_length=255, null=True, blank=True)
    location = models.TextField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Deactivate', 'Deactivate')],null=True, blank=True)
    package = models.CharField(max_length=20, choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three')],null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.company_name 

    def save(self, *args, **kwargs):
        if not self.company_name:
            self.company_name = "Unchanged"
        super().save(*args, **kwargs)
    
class client(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clients' , null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone1 = models.CharField(max_length=15,null=True, blank=True)
    email1 = models.EmailField(null=True, blank=True)
    address1 = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return self.name or "Unnamed Client"
    

class Gate(models.Model) :
    client = models.ForeignKey(client, on_delete=models.CASCADE, related_name='gates', null=True, blank=True)
    select_client = models.CharField(max_length=255, null=True, blank=False )
    items = models.TextField( null=True, blank=True)
    units = models.TextField( null=True, blank=True)
    type = models.EmailField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)    

    def __str__(self):
        return self.items or "Unnamed Client"

class Storage(models.Model):
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='storages', null=True, blank=True)
    select_client = models.CharField(max_length=255 ,null=True, blank=False)
    items = models.TextField( null=True, blank=True)
    old_weight = models.FloatField(null=True, blank=True)
    new_weight = models.FloatField(null=True, blank=True)
    chamber = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)
    from_blocks = models.CharField(max_length=255, null=True, blank=True)
    to_blocks = models.CharField(max_length=255, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    payable_amount = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return self.items
    
class Block_Setting(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='blocks', null=True, blank=True)
    store = models.TextField(null=True, blank=False)
    chamber = models.CharField(max_length=15, null=True, blank=True)
    temprature = models.EmailField(null=True, blank=True)
    floor = models.TextField(null=True, blank=True)
    block_no = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)    

    def __str__(self):
        return self.store or "Unnamed Store"

class Admin(models.Model):
    package = models.TextField( null=True, blank=False )
    duration = models.CharField(max_length=15, null=True, blank=True)
    price = models.EmailField(null=True, blank=True)
    capacity = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)   

    def __str__(self):
        return self.package or "Unnamed Package"
    

class ColdStoreEntry(models.Model):
    client = models.ForeignKey(client, on_delete=models.CASCADE, related_name='cold_store_entries', null=True, blank=True)
    full_name = models.CharField(max_length=255 ,default="Unnamed Client", null=True, blank=True)
    phone = models.CharField(max_length=20)
    item_type = models.CharField(max_length=100)
    address = models.TextField()
    weight_at_gate = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return self.full_name or "Unnamed Owner"
      
class store(models.Model):
    store_name = models.TextField(null=True, blank=True, default="Unnamed Client")
    manager = models.CharField(max_length=255 ,null=True, blank=False )
    phone2 = models.CharField(max_length=15,null=True, blank=True)
    email2= models.EmailField(max_length=255 ,null=True, blank=True)
    address2 = models.CharField(max_length=255 ,null=True, blank=True)
    temprature1 = models.CharField(max_length=50, choices=[("Normal", "Normal"), ("Cold", "Cold"), ("Hot", "Hot")],null=True, blank=True)
    chamber_no = models.CharField(max_length=255,null=True, blank=True)
    capacity = models.CharField(max_length=255 ,null=True, blank=True)
    chamber_details = models.JSONField(default=list)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return self.store_name or "Unnamed store name"
    
class Package(models.Model):
    DURATION_CHOICES = [
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
        ('1 Year', '1 Year'),
        ('2 Years', '2 Years'),
        ('5 Years', '5 Years'),
    ]

    name = models.TextField(null=True, blank=True, default="Undefined Package")
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    price = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.duration}"  # Return a string representation


class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name or "Unnamed Item Name"
    

