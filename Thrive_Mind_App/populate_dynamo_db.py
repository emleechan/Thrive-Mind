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
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    email_address = UnicodeAttribute()
    phone_number = UnicodeAttribute()
    is_accepting = BooleanAttribute()

# Create database in dynamodb if it doesnt already exist :)
if not HealthcareServiceModel.exists():
    HealthcareServiceModel.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

    service1 = HealthcareServiceModel(str(uuid.uuid4()), name="healthcareservice1", description="This is a description of healthcare service 1", email_address="service1@healthcare.com", phone_number="(101) 301-0485", is_accepting=True)
    service2 = HealthcareServiceModel(str(uuid.uuid4()), name="healthcareservice2", description="This is a description of healthcare service 2", email_address="service2@healthcare.com", phone_number="(202) 321-2485", is_accepting=False)
    service3 = HealthcareServiceModel(str(uuid.uuid4()), name="someotherservice", description="This is a description of a different service", email_address="service3@somethingelse.com", phone_number="(666) 666-6666", is_accepting=True)

    service1.save()
    service2.save()
    service3.save()


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

