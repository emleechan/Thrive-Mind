import boto3
import pynamodb
import uuid
import json

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

class HealthcareServiceModel(Model):
    """
    A HealthcareService service
    """
    class Meta:
        table_name = 'healthcareservice-service'
        region = 'us-east-1'
    hid = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    email_address = UnicodeAttribute()
    phone = UnicodeAttribute()
    is_accepting = BooleanAttribute()

# Create database in dynamodb if it doesnt already exist :)
if not HealthcareServiceModel.exists():
    HealthcareServiceModel.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

    service = HealthcareServiceModel(str(uuid.uuid4()), name="SFU Counseling", description="Find a counselor today, covered by your student insurance, today!", email_address="sfucounseling@sfu.ca", phone="(101) 301-0485", is_accepting=True)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="ABC Private Counseling", description="Don't settle for second-best public counseling from a school... go private!", email_address="ABC@private.com", phone="(202) 321-2485", is_accepting=False)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="Surrey Memorial Hospital", description="This is where you go if you get seriously hurt :/", email_address="surreym@hospital.com", phone="(666) 666-6666", is_accepting=True)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="Travel Medical Clinic", description="Going on vacation? Get your vac(cin)ations!", email_address="travelmedical@vaccinations.com", phone="(778) 434-3102", is_accepting=True)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="COVID-19 Test Drive-Thru", description="Fever? Headache? Shortness of breath? Come test yourself safely, here!", email_address="covid19@humanityisdoomed.com", phone="(604) 123-4567", is_accepting=False)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="CoronaVirus Info Center", description="Don't listen to the media, get your state-sponsored 'facts' here!", email_address="coronavirus@isnotreal.com", phone="(987) 654-2934", is_accepting=True)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="healthcareservice1", description="This is a description of healthcare service 1", email_address="service1@healthcare.com", phone="(101) 301-0485", is_accepting=True)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="healthcareservice2", description="This is a description of healthcare service 2", email_address="service2@healthcare.com", phone="(202) 321-2485", is_accepting=False)
    service.save()
    service = HealthcareServiceModel(str(uuid.uuid4()), name="someotherservice", description="This is a description of a different service", email_address="service3@somethingelse.com", phone="(666) 666-6666", is_accepting=True)
    service.save()


# INSERT PATIENT DB CREATION STUFF HERE
class PatientModel(Model):
   class Meta:
       table_name = "healthcareservice-patient"
       region = 'us-east-1'
       read_capacity_units = 1
       write_capacity_units = 1
   pid = UnicodeAttribute(hash_key=True)
   first_name =  UnicodeAttribute()
   last_name = UnicodeAttribute()
   user_email = UnicodeAttribute()
   user_password = UnicodeAttribute()
   email_address = UnicodeAttribute()
   is_seeking = BooleanAttribute()
   phone = UnicodeAttribute()
   medical_history = UnicodeAttribute()
   current_prescription = UnicodeAttribute()
   preferences = UnicodeAttribute()
   health_care_plan = UnicodeAttribute()

if not PatientModel.exists():
    PatientModel.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

