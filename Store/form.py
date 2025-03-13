# forms.py
from django import forms
from .models import Package
from .models import Custom        
from .models import Company
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'duration', 'price', 'capacity']
class ManagerForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = ['username', 'password', 'email']

class GateManagerForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = ['username', 'password', 'email']
        
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'owner_firm_manager', 'phone', 'email', 'address', 'experience', 'location', 'status', 'package', 'from_date', 'to_date', 'about']