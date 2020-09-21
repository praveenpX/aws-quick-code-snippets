from __future__ import print_function
import boto3
import json

def lambda_handler(event, context):
    print ("sqs lambda function is being called...")
    
    #get the kinesis batch metadata
    
    for record in event['Records']:
       payload=record["body"]
       
       jsonData = json.loads(payload)
       
       print(jsonData)
       
    rshardId = jsonData['KinesisBatchInfo']['shardId']
    rstreamName = 'my-data-stream'
    rstartSequenceNumber = jsonData['KinesisBatchInfo']['startSequenceNumber']
    rendSequenceNumber = jsonData['KinesisBatchInfo']['endSequenceNumber']
    rbatchSize = jsonData['KinesisBatchInfo']['batchSize']
    
    #use the meta data to get the iterator
      
    client = boto3.client('kinesis')

    kresponse = client.get_shard_iterator(
                    StreamName= rstreamArn,
                    ShardId= rshardId,
                    ShardIteratorType='AT_SEQUENCE_NUMBER',
                    StartingSequenceNumber= rstartSequenceNumber
            )
    
    shardIteratorJsonDataDump = json.dumps(kresponse)
    
    shardIteratorJsonData = json.loads(shardIteratorJsonDataDump)
        
    shardIteratorDataId = shardIteratorJsonData['ShardIterator']
        
    print('iteratorid: ' + shardIteratorDataId)
    
    #use the iterator to get the kinesis records
    
    kinesisErrorRecords = client.get_records(
                    ShardIterator= shardIteratorDataId,
                    Limit= rbatchSize
    )
    
    print(str(kinesisErrorRecords))

    


    
