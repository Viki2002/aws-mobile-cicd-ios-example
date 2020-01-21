#!/usr/bin/env python

import boto3
import tempfile
import zipfile

cp = boto3.client('codepipeline')

def handle_job(job):

    # Acknowledge the job
    cp.acknowledge_job(
       jobId = job['id'],
       nonce = job['nonce']
    )

    # Configure S3 with the artifact credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id=job['data']['artifactCredentials']['accessKeyId'],
        aws_secret_access_key=job['data']['artifactCredentials']['secretAccessKey'],
        aws_session_token=job['data']['artifactCredentials']['sessionToken']
    )

    # Download the input artifact
    input_artifact_s3_location = job['data']['inputArtifacts'][0]['location']['s3Location']
    _, input_artifact = tempfile.mkstemp()
    s3.download_file(input_artifact_s3_location['bucketName'], input_artifact_s3_location['objectKey'], input_artifact)
    print(input_artifact)

    # Exctract the input artifact
    build_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(input_artifact, 'r') as zr:
        zr.extractall(build_dir)
    print(build_dir)

    cp.put_job_failure_result(
        jobId = job['id'],
        failureDetails={
            'type' : 'JobFailed',
            'message' : 'BUILD FAILED'
        }
    )
    


def main():
    while(True):

        # Poll for jobs
        poll_result = cp.poll_for_jobs(
            actionTypeId={
                'category' : 'Build',
                'owner' : 'Custom',
                'provider' : 'AppleXCode',
                'version' : '1'
            },
            maxBatchSize=1
        )

        for job in poll_result['jobs']:
            print(job)
            handle_job(job)
        
        break

if __name__=="__main__":
    main()
