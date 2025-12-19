
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from configurator.models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Resets DB and generates specific test data: users vlad_1..100 and 10 requests each'

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        self.stdout.write('Starting data reset and generation...')

        
        self.stdout.write('Deleting all existing users and data...')
        User.objects.all().delete()
        
       

        self.stdout.write('Creating 100 users (vlad_1 to vlad_100)...')
        users = []
        for i in range(1, 101):
            username = f'vlad_{i}'
            password = 'vlad123'
            
            if i == 1:
                user = User.objects.create_superuser(
                    username=username,
                    email=f'{username}@example.com',
                    password=password
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password=password
                )
            users.append(user)

 
        
    
        comp_types = ['CPU', 'GPU', 'Motherboard', 'RAM', 'Storage', 'Power Supply', 'Case']
        type_objs = {}
        for ct_name in comp_types:
            ct, created = ComponentType.objects.get_or_create(name=ct_name)
            type_objs[ct_name] = ct

   
        self.stdout.write('Generating manufacturers...')
        manufacturers = []
        for _ in range(5):
            m = Manufacturer.objects.create(
                name=fake.company(),
                user=random.choice(users), 
                country=fake.country(),
                website=fake.url()
            )
            manufacturers.append(m)

     
        self.stdout.write('Generating components...')
        components_by_type = {ct: [] for ct in type_objs.values()}
        for ct_name, ct_obj in type_objs.items():
            for _ in range(10): 
                comp = Component.objects.create(
                    name=f"{ct_name} {fake.word().upper()} {fake.random_number(digits=4)}",
                    user=random.choice(users),
                    component_type=ct_obj,
                    manufacturer=random.choice(manufacturers),
                    price=random.randint(1000, 100000),
                    description=fake.text(),
                    in_stock=True
                )
                components_by_type[ct_obj].append(comp)

        self.stdout.write('Generating PC configurations...')
        configurations = []
        for _ in range(30): 
            try:
                config = PCConfiguration.objects.create(
                    name=fake.catch_phrase(),
                    user=random.choice(users),
                    description=fake.text(),
                    cpu=random.choice(components_by_type[type_objs['CPU']]),
                    gpu=random.choice(components_by_type[type_objs['GPU']]),
                    motherboard=random.choice(components_by_type[type_objs['Motherboard']]),
                    ram=random.choice(components_by_type[type_objs['RAM']]),
                    storage=random.choice(components_by_type[type_objs['Storage']]),
                    power_supply=random.choice(components_by_type[type_objs['Power Supply']]),
                    case=random.choice(components_by_type[type_objs['Case']])
                )
                configurations.append(config)
            except IndexError:
                 continue

        if not configurations:
            self.stdout.write(self.style.ERROR("Failed to generate configurations"))
            return

        
        self.stdout.write('Generating 10 BuildRequests per user...')
        objs = []
        for user in users:
            for _ in range(10):
                objs.append(BuildRequest(
                    user=user,
                    configuration=random.choice(configurations),
                    status=random.choice(['pending', 'in_progress', 'completed', 'cancelled']),
                    budget=random.randint(50000, 500000),
                    notes=fake.sentence()
                ))
        
        BuildRequest.objects.bulk_create(objs)
     
        self.stdout.write(self.style.SUCCESS('--------------------------------------------------'))
        self.stdout.write(self.style.SUCCESS(f'Total Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Superuser: {User.objects.get(username="vlad_1").username} (is_superuser={User.objects.get(username="vlad_1").is_superuser})'))
        self.stdout.write(self.style.SUCCESS(f'Total Requests: {BuildRequest.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('--------------------------------------------------'))
