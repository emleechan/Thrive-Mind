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


def services_get(event, context):
    services = []
    for item in HealthcareServiceModel.scan(limit=20):
        services.append(item.attribute_values)

    ret = { 'services': services }

    return ret
