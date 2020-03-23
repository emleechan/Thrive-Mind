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
       table_name = "patient"
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
 
 
def lambda_handler(event, context):
   patient_item = Patient.get(event['pid'])
   return {
       'statusCode': 200,
       'body': json_dumps(patient_item)
   }
