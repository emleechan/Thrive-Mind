import boto3
import pynamodb
import uuid
import json

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class HealthcareServiceModel(Model):
    """
    A HealthcareService service
    """
    class Meta:
        table_name = 'healthcareservice-service-PI3'
        region = 'us-east-1'
    hid = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    email_address = UnicodeAttribute()
    phone = UnicodeAttribute()
    is_accepting = BooleanAttribute()

#probably don't actually need this.
class ViewIndex(GlobalSecondaryIndex):
    #This represents a global secondary index
    class Meta:
        index_name='srch-index'
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

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

#search function will check each attribute and return all that exist
def services_search(event, context):
    #service_item = HealthcareServiceModel.get(event['queryStringParameters']['someSearchKey'])
    services = []
    query = event['queryStringParameters']['someSearchKey']
    print("this is the search value: ",query)
    try:
        print("Will this show in log?")
        for item in HealthcareServiceModel.scan(HealthcareServiceModel.name.contains(query) | HealthcareServiceModel.description.contains(query) | HealthcareServiceModel.email_address.contains(query) | HealthcareServiceModel.phone.contains(query)):
            services.append(item.attribute_values)
        ret = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials" : True},
            "body": json.dumps(services)
        }
        return ret
    except:
        print("Search of model failed")
    else:
        print("No issues here")
    