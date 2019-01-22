import json
import uuid
import boto3

clientTranscribe = boto3.client('transcribe')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    audiofileS3='https://s3-eu-west-1.amazonaws.com/' + bucket + '/' + key
    
    outputBucket= 'interpreter-demo-transcriptions-output'
    
    print("Uri S3 file: " + audiofileS3)
    
    response = clientTranscribe.start_transcription_job(
        TranscriptionJobName='interpreterDemoTranscribe-'+str(uuid.uuid4()),
        LanguageCode='it-IT',
        MediaFormat='mp4',
        Media={
            'MediaFileUri': audiofileS3
        },
        OutputBucketName=outputBucket,
        Settings={
            #'VocabularyName': 'interpreterDemoVocabulary',
            'ShowSpeakerLabels': False,
            'ChannelIdentification': False
        }
    )
    
    return 'ok'
