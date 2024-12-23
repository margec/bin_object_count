import json
import boto3

def lambda_handler(event, context):
    # TODO implement

    print('capstone-function is called...')
    print(event)

    default_endpoint_name = 'pytorch-inference-2024-12-19-20-03-10-736'

    body = event.get('body')
    if body is not None:
        # from API 
        new_event = json.loads(body)
    else:
        # from Test
        new_event = event
    
    endpoint_name = new_event.get('endpoint_name', default_endpoint_name)
    s3_uri = new_event['s3_uri']

    sm_runtime = boto3.Session().client('sagemaker-runtime')
    
    response = sm_runtime.invoke_endpoint(EndpointName=endpoint_name,
                                    ContentType="application/json",
                                    Accept='application/json',
                                    #Body=bytearray(x)
                                    Body=json.dumps(event))
    
    result_text = response['Body'].read().decode('utf-8')
    result = json.loads(result_text)
    max_index = result[0].index(max(result[0]))

    prediction = {
        'event': event,
        'inference_response': result,
        'prediction_class': max_index + 1
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(prediction)
    }
