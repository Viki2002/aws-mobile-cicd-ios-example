#!/usr/bin/env python

import boto3

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
        aws_access_key_id=job['data']['artifactCredentials']['accessKeyId']
        aws_secret_access_key=job['data']['artifactCredentials']['secretAccessKey'],
        aws_session_token=job['data']['artifactCredentials']['sessionToken']
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
            handle_job(job)
        
        break

if __name__=="__main__":
    main()
