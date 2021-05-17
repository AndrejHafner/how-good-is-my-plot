import sys
import boto3

from utils import get_mt_client, environments

client = get_mt_client()
# Test that you can connect to the API by checking your account balance
user_balance = client.get_account_balance()

# In Sandbox this always returns $10,000. In live, it will be your acutal balance.
print("Your account balance is {}".format(user_balance['AvailableBalance']))

# The question we ask the workers is contained in this file.
question_sample = open("question_ui.xml", "r").read()

# Example of using qualification to restrict responses to Workers who have had
# at least 80% of their assignments approved. See:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs
worker_requirements = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [80],
    'RequiredToPreview': True,
}]

# Create the HIT
response = client.create_hit(
    MaxAssignments=3,
    LifetimeInSeconds=600,
    AssignmentDurationInSeconds=600,
    Reward="0.00",
    Title="Plot comparisons - test",
    Keywords='question, answer, research',
    Description='Answer a simple question. Created from mturk-code-samples.',
    Question=question_sample,
    QualificationRequirements=worker_requirements
    # HITLayoutParameters=[
    #     {"Name": "n_plots", "Value": "3"}
    # ]
)

# The response included several fields that will be helpful later
hit_type_id = response['HIT']['HITTypeId']
hit_id = response['HIT']['HITId']
print("\nCreated HIT: {}".format(hit_id))

print("\nYou can work the HIT here:")
print(environments["sandbox"]['preview'] + "?groupId={}".format(hit_type_id))
print("\nAnd see results here:")
print(environments["sandbox"]['manage'])