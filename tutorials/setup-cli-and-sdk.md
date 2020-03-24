## Setup Credentials File
To run either the AWS CLI or an AWS language SDK (boto3 for python, java SDK, etc.) you must setup the credentials these will use to access the AWS API.

1. Navigate to the labs.vocareum.com page where you normally open the AWS console. Click the "Account Details" button.
<image src="images/setup-cli-and-sdk-1.png" />
1. This should bring up an modal that displays your current session details. Click the "Show" button to display the AWS CLI/API credentials.
<image src="images/setup-cli-and-sdk-2.png" />
1. This should show credentials that look like the following.
<image src="images/setup-cli-and-sdk-3.png" />
1. Now, in a terminal session, run these commands: 
```
# create the .aws directory
$ mkdir -p ~/.aws

# remove any existing credentials file
$ rm -f ~/.aws/credentials

# create the credentials file
$ touch ~/.aws/credentials

# edit the credentials file with whatever editor you're comfortable with
$ vi ~/.aws/credentials

# Paste the credentials from the vocareum site and save the file.
```
5. These credentials will be valid for the length of your session, which is about 4 hours. When they expire, you will have to re-edit the credentials file and replace them with new tokens from the vocareum site.

## Setup Python SDK (boto3)
The python SDK (named boto3) is how all of our python code will interact with AWS services, such as querying dynamo db or cognito.
1. Ensure you have python 3 installed on your machine
1. Run this to install or upgrade to the latest version of boto3:
    * `$ pip3 install --upgrade boto3`
1. Thats it! It should automatically pick it up with the credentials file. Test it with some example code to verify:
```
import boto3

s3 = boto3.resource('s3')
buckets = [bucket.name for bucket in s3.buckets.all()]
print(buckets)
```
4. It should print an empty list `[]`, with no error.

## Setup AWS CLI
1. just follow the instructions on https://docs.aws.amazon.com/cli/latest/userguide/install-cliv1.html. It's easier to install aws cli version 1 than version 2; so let's stick with that! 
1. Once installed it should automatically pick up your credentials. Test it with:
```
$ aws s3api list-buckets --query "Buckets[].Name"
```

3. It should return an empty list `[]`; you should see no error.