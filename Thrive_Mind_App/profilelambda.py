import boto3
import json
import decimal
from pynamodb.models import Model
from pynamodb.attributes import (
   UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
)
 
class ModelEncoder(json.JSONEncoder):
   def default(self, obj):
       if hasattr(obj, 'attribute_values'):
           return obj.attribute_values
       elif isinstance(obj, datetime.datetime):
           return obj.isoformat()
       return json.JSONEncoder.default(self, obj)
 
def json_dumps(obj):
   return json.dumps(obj, cls=ModelEncoder)
 
class Patient(Model):
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
 
 
def profile_get(event, context):
   patient_item = Patient.get(event['pid'])
   
   ret = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials" : True},
        "body": json_dumps(patient_item)
    }

   return ret

def profile_update(event, context):
    patient_item = Patient.get(event['pid'])
    patient_item.update(actions=[
        Patient.first_name.set(event['first_name']),
        Patient.last_name.set(event['last_name']),
        Patient.user_password.set(event['user_password']),
        Patient.email_address.set(event['email_address']),
        Patient.phone.set(event['phone']),
        Patient.is_seeking.set(event['is_seeking']),
        Patient.medical_history.set(event['medical_history']),
        Patient.current_prescription.set(event['current_prescription']),
        Patient.preferences.set(event['preferences']),
        Patient.health_care_plan.set(event['health_care_plan'])
    ])
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials" : True},
        "body": json_dumps(patient_item)
   }
