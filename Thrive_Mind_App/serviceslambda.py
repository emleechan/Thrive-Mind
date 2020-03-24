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


def services_get(event, context):
    print(event)
    services = []
    for item in HealthcareServiceModel.scan(limit=20):
        services.append(item.attribute_values)

    ret = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials" : True},
        "body": json.dumps(services)
    }

    return ret
