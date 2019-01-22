import json
import boto3
import os
from contextlib import closing
import uuid

clientS3 = boto3.client('s3')
clientTranslate = boto3.client('translate')
clientPolly = boto3.client('polly')

# Main Handler
def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    data = clientS3.get_object(Bucket=bucket, Key=key, ResponseContentEncoding='utf-8')

    transcribeJson = json.loads(str(data['Body'].read()))

    textToTranslate = transcribeJson['results']['transcripts'][0]['transcript'] 

    print('Text to be transalted: '+ textToTranslate)
     
    translationResult = clientTranslate.translate_text(
                Text=textToTranslate, 
                SourceLanguageCode="it", 
                TargetLanguageCode="en"
            )
            
    translatedSentence=translationResult.get('TranslatedText')
            
    print('Transalted Text: ' + translatedSentence)
    
    # send result to polly
    voiceAudio = clientPolly.synthesize_speech(
                VoiceId='Brian',
                OutputFormat='mp3',
                Text = translatedSentence)

    print('Polly synthesis executed...')

    outputFileID='temporary.mp3'
    #Save the audio stream returned by Amazon Polly on Lambda's temp 
    # directory. If there are multiple text blocks, the audio stream
    # will be combined into a single file.
    print('Start reading audio stream...')
    if "AudioStream" in voiceAudio:
        with closing(voiceAudio["AudioStream"]) as stream:
            output = os.path.join("/tmp/", outputFileID)
            with open(output, "a") as file:
                file.write(stream.read())

    print ('Audio stream reading ended...')
    outputBucket='interpreter-demo-files'
    outputFileKey="audio-output/TranslatedAudio-" + str(uuid.uuid4()) + ".mp3"

    print('Start uploading audio file on S3')
    clientS3.upload_file('/tmp/' + outputFileID, 
      outputBucket,
      outputFileKey)
      
    print('File uploaded. Starting setting up ACL')  
    clientS3.put_object_acl(ACL='public-read', 
      Bucket=outputBucket, 
      Key=outputFileKey)    
      
    os.remove(os.path.join("/tmp/", outputFileID))
    
    print('Function demo transalte successfully completed.')
    return 'ok'
