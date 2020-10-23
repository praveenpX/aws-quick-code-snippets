"""
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 
"""


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

    


    
