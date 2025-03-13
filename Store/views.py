from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Company,client,Gate,Storage,Block_Setting,Admin,ColdStoreEntry,store,Custom ,Package, Item
from django.utils.dateparse import parse_date
from django.views.generic import CreateView
from .models import Custom
from .form import ManagerForm, GateManagerForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .mixins import AdminRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='Login')
def dashboard(request):
    user = request.user 
    return render(request, 'dashboard.html', {'user': user})


def generate_random_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@login_required(login_url='Login')
def Register(request):
    # Fetch all packages from the database
    packages = Package.objects.all()

    if request.method == 'POST':
        # Extract data from the form
        company_name = request.POST.get('Company_Name')
        owner_firm_manager = request.POST.get('Owner_Firm_Manager')
        phone = request.POST.get('Phone')
        email = request.POST.get('Email')
        address = request.POST.get('Address')
        experience = request.POST.get('Experience')
        location = request.POST.get('Location')
        status = request.POST.get('Status')
        package = request.POST.get('Package')
        from_date_str = request.POST.get('From_Date')
        to_date_str = request.POST.get('To_Date')
        about = request.POST.get('About')
        from_date = parse_date(from_date_str) if from_date_str else None
        to_date = parse_date(to_date_str) if to_date_str else None

        try:
            # Save the company to the database
            company = Company.objects.create(
                company_name=company_name,
                owner_firm_manager=owner_firm_manager,
                phone=phone,
                email=email,
                address=address,
                experience=experience,
                location=location,
                status=status,
                package=package,
                from_date=from_date,
                to_date=to_date,
                about=about,
                user=request.user,
            )

            # Create an admin user for the company
            User = get_user_model()
            username = phone  
            password = generate_random_password()  
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=User.Role.ADMIN
            )
            company = Company.objects.all()

            # Send email with credentials
            subject = 'Your Admin Credentials'
            message = f"""
            Hello {owner_firm_manager},

            Your company {company_name} has been successfully registered.
            Here are your admin credentials:
            Username: {username}
            Password: {password}

            Please keep this information secure.
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            company = Company.objects.filter(user=request.user)
            messages.success(request, f"Company registered successfully. Admin credentials have been sent to {email}.")
            return render(request, 'company_register.html', {'registers': company, 'packages': packages})

        except Exception as e:
            print(f"Error saving company or creating admin user: {e}")
            messages.error(request, "An error occurred while registering the company.")
            return render(request, 'company_register.html', {'packages': packages})

    # Render the form with packages
    registers = Company.objects.all()
    return render(request, 'company_register.html', {'registers':registers ,'packages': packages})

@login_required(login_url='Login')
def Staff(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = Custom.objects.create_user(username=username, email=email, password=password, role=role)
        user.save()
        messages.success(request, f"User {username} registered successfully as {role}!")
        return redirect("Staff")

    return render(request, "Staff.html")


@login_required(login_url='Login')
def Store(request):
    if request.method == 'POST':
        # Extract data from the form
        store_name = request.POST.get('Store_Name')
        manager = request.POST.get('Manager')
        phone2 = request.POST.get('Phone2')
        email2 = request.POST.get('Email2')
        address2 = request.POST.get('Address2')
        temperature1 = request.POST.get('Temprature1')
        capacity = request.POST.get('Capacity')
        chamber_no = request.POST.get('Chamber_no')

        # Initialize chamber_block_structure
        chamber_block_structure = []

        try:
            chamber_no = int(chamber_no) if chamber_no and int(chamber_no) > 0 else 1
            for chamber in range(1, chamber_no + 1):
                floor_no_key = f"floor_no_{chamber}"
                floor_no = int(request.POST.get(floor_no_key, 1))

                floors = []
                for floor in range(1, floor_no + 1):
                    block_no_key = f"block_no_{chamber}_{floor}"
                    block_no = int(request.POST.get(block_no_key, 1))
                    blocks = []
                    for block in range(1, block_no + 1):
                        block_size_key = f"block_size_{chamber}_{floor}_{block}"
                        block_size = int(request.POST.get(block_size_key, 100))

                        blocks.append({
                            "block_name": f"Block {chr(65 + block - 1)}",
                            "block_size": block_size,
                        })

                    floors.append({
                        "floor_name": f"Floor {floor}",
                        "blocks": blocks,
                    })

                chamber_block_structure.append({
                    "chamber_name": f"Chamber {chamber}",
                    "temperature": request.POST.get(f"temperature_{chamber}"),  
                    "floors": floors,
                })

            # Save store details with chamber_block_structure
            stores = store.objects.create(
                store_name=store_name,
                manager=manager,
                phone2=phone2,
                email2=email2,
                address2=address2,
                temprature1=temperature1,
                chamber_no=chamber_no,
                capacity=capacity,
                chamber_details=chamber_block_structure,
                user=request.user,  
            )
            stores.objects.all()

            messages.success(request, "Store registered successfully!")
            return redirect('Chamber')  

        except Exception as e:
            print(f"Error saving Store details: {e}")
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'add_store.html', {
                'chamber_block_structure': chamber_block_structure,  
            })

    # Fetch stores associated with the current user
    stores = store.objects.filter(user=request.user).all()
    return render(request, 'add_store.html', {'stores': stores})

@login_required(login_url='Login')
def Client(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        phone1 = request.POST.get('Phone1')
        email1 = request.POST.get('Email1')
        address1 = request.POST.get('Address1')
        file = request.FILES.get('Add File')

        try:
            # Save the data to the database
            client.objects.create(
                name=name,
                phone1=phone1,
                email1=email1,
                address1=address1,
                file=file,
                user=request.user,
            )

           
            messages.success(request, "Client registered successfully!" )
            return redirect('Inventory_Gate')

        except Exception as e:
            print(f"Error saving Client: {e}") 
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'add_client.html')
    return render(request, 'add_client.html')

@login_required(login_url="Login")
def Inventory_Gate(request):
    if request.method == 'POST':
        select_client_id = request.POST.get('Select_Client')  
        item_id = request.POST.get('Select_Item')  
        units = request.POST.get('Units')
        type = request.POST.get('Types')
        weight = request.POST.get('Weight')
        from_date = request.POST.get('Date')

        print(f"Received Item ID: {item_id}") 

        try:
            if not select_client_id or not item_id:
                messages.error(request, "Client or Item not selected.")
                return redirect('Inventory_Gate')

            select_client_id = int(select_client_id)
            item_id = int(item_id)

            if not client.objects.filter(id=select_client_id).exists():
                messages.error(request, "Selected client does not exist.")
                return redirect('Inventory_Gate')

            if not Item.objects.filter(id=item_id).exists():
                messages.error(request, "Selected item does not exist.")
                return redirect('Inventory_Gate')

            select_client = client.objects.get(id=select_client_id)
            selected_item = Item.objects.get(id=item_id)

            gate_entry = Gate.objects.create(
                select_client=select_client,  
                items=selected_item,
                units=units,
                type=type,
                weight=weight,
                from_date=from_date,
                user=request.user,
            )
            messages.success(request, "Registered successfully!")
            return render(request, 'gate_receipt.html', {'entry': gate_entry})

        except ValueError:
            messages.error(request, "Invalid client or item ID.")
        except Exception as e:
            print(f"Error saving data: {e}")  
            messages.error(request, "An error occurred while registering.")

    clients = client.objects.all()
    items = Item.objects.all()
    inventories = Gate.objects.all()
    
    return render(request, 'add_inventory_gate.html', {'clients': clients, 'items': items, 'inventories': inventories})

@login_required(login_url='Login')
def Inventory(request, old_weight=None):  
    if request.method == 'POST':
        select_client_id = request.POST.get('Select_Client')
        items_id = request.POST.get('Select_Item')
        new_weight = request.POST.get('Weight_at_Storage')
        chamber = request.POST.get('Select_Chamber')
        floor = request.POST.get('Select_Floor')
        from_blocks = request.POST.get('Select_From_Block')
        to_blocks = request.POST.get('To_Block')
        rate = request.POST.get('Rate')
        duration_id = request.POST.get('Select_Duration')
        payable_amount = request.POST.get('Payable_Amount')
        paid_amount = request.POST.get('Amount_Paid')
        from_date = request.POST.get('Date')

        try:
            select_client = client.objects.get(id=select_client_id)
            items = Item.objects.get(id=items_id)
            duration = Package.objects.get(id=duration_id)

            last_gate_entry = Gate.objects.filter(select_client=select_client, items=items).order_by('-id').first()
            old_weight = last_gate_entry.weight if last_gate_entry else 0  
         
            inventories=Storage.objects.create(
                select_client=select_client,
                items=items,
                old_weight=old_weight,  
                new_weight=new_weight,
                chamber=chamber,
                floor=floor,
                from_blocks=from_blocks,
                to_blocks=to_blocks,
                rate=rate,
                duration=duration,
                payable_amount=payable_amount,
                paid_amount=paid_amount,
                from_date=from_date,
                user=request.user,
            )

            messages.success(request, "Inventory registered successfully!")
            return redirect('Recipt') 

        except client.DoesNotExist:
            messages.error(request, "Selected client does not exist.")
        except Item.DoesNotExist:
            messages.error(request, "Selected item does not exist.")
        except Package.DoesNotExist:
            messages.error(request, "Selected duration package does not exist.")
        except Exception as e:
            print(f"Error saving Inventory details: {e}")
            messages.error(request, "An error occurred while registering the inventory.")

        context = {
            'clients': client.objects.all(),
            'items': Item.objects.all(),
            'packages': Package.objects.all(),
            'form_data': request.POST, 
            'old_weight': old_weight, 
        }
        return render(request, 'add_inventory.html', context)

    clients = client.objects.all()
    items = Item.objects.all()
    packages = Package.objects.all()
    inventories = Storage.objects.all()

    if old_weight is None and request.GET.get('client_id') and request.GET.get('item_id'):
        try:
            select_client = client.objects.get(id=request.GET.get('client_id'))
            selected_item = Item.objects.get(id=request.GET.get('item_id'))
            last_gate_entry = Gate.objects.filter(select_client=select_client, items=selected_item).order_by('-id').first()
            old_weight = last_gate_entry.weight if last_gate_entry else 0
        except client.DoesNotExist:
            old_weight = 0  

    context = {
        'clients': clients,
        'items': items,
        'packages': packages,
        'old_weight': old_weight,
        'inventories': inventories
    }

    return render(request, 'add_inventory.html', context)


@login_required(login_url='Login')
def Setting(request):
    if request.method == 'POST':
        store = request.POST.get('Store')
        chamber = request.POST.get('Chamber')
        temprature = request.POST.get('Temprature')
        floor = request.POST.get('Floor')
        block_no = request.POST.get('Block_no')

        try:
            # Save the data to the database
            Block_Setting.objects.create(
                store=store,
                chamber=chamber,
                temprature=temprature,
                floor=floor,
                block_no=block_no,
                user=request.user,
            )
           
            messages.success(request, "Blocks registered successfully!")
            return redirect('Admin_Setting')

        except Exception as e:
            print(f"Error saving Client: {e}")  
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'settings.html')
    return render(request, 'settings.html')

@login_required(login_url='Login')

def admin_settings(request):
    packages = Package.objects.all()
    items = Item.objects.all()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'package_form':
            package_name = request.POST.get('Package_Name')
            duration = request.POST.get('Duration')
            price = request.POST.get('price')
            capacity = request.POST.get('capacity')

            try:
                Package.objects.create(
                    name=package_name,
                    duration=duration,
                    price=price,
                    capacity=capacity,
                )
                messages.success(request, "Package added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding package: {e}")

        elif form_type == 'item_form':
            # Handle Item Form Submission
            item_name = request.POST.get('Item_Name')
            quantity = request.POST.get('quantity')

            try:
                Item.objects.create(
                    name=item_name,
                    quantity=quantity,
                )
                messages.success(request, "Item added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding item: {e}")

        return redirect('Admin_Setting') 

    return render(request, 'admin-settings.html', {
        'packages': packages,
        'items': items,
    })
@login_required(login_url='Login')
def Recipts(request):

    latest_entry = ColdStoreEntry.objects.last() 

    return render(request, 'gate_receipt.html', {'entry': latest_entry})

@login_required(login_url='Login')
def Details(request):
    return render(request, 'client_details.html')

@login_required(login_url='Login')
def Chamber(request):
    store_instance = store.objects.filter(user=request.user).last()
    chamber_block_structure = store_instance.chamber_details if store_instance else []

    return render(request, 'chamber.html', {
        'chamber_block_structure': chamber_block_structure,
    })

def sidebar_view(request):
    return render(request, 'sidebar.html')


# View for creating a Manager
class CreateManagerView(AdminRequiredMixin, CreateView):
    model = Custom
    form_class = ManagerForm
    template_name = 'Staff.html'
    success_url = reverse_lazy('manager_list')  
    
    def form_valid(self, form):
        form.instance.role = Custom.Role.MANAGER
        form.instance.company_name = self.request.user.company_name  
        return super().form_valid(form)

class CreateGateManagerView(AdminRequiredMixin, CreateView):
    model = Custom
    form_class = GateManagerForm
    template_name = 'Staff.html'
    success_url = reverse_lazy('gate_manager_list')  
    
    def form_valid(self, form):
        form.instance.role = Custom.Role.GATE_MANAGER
        form.instance.company_name = self.request.user.company_name
        return super().form_valid(form)
