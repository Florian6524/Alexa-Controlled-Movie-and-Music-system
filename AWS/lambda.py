import json
import boto3

client = boto3.client('iot-data', region_name='eu-west-1')

def lambda_handler(event, context):
    print(event)
    response = client.publish(
        topic='pico_Florian_topic',
        qos=1,
        payload=json.dumps(event['request']['intent']['name'])
    )
    print(response)
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Okay"
            },
            "shouldEndSession": True
        }
    }
