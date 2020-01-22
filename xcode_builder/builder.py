#!/usr/bin/env python

import boto3
import tempfile
import zipfile
import subprocess
import os
import glob
import traceback
import sys
import time
from os.path import basename

cp = boto3.client('codepipeline')
SLEEP_TIME = 15 # Number of seconds to sleep between each poll

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

    pwd = os.getcwd()
    os.chdir(build_dir)
    exit_code = subprocess.call(["make", "all"])
    os.chdir(pwd)
    if exit_code != 0:
        raise Exception("BUILD FAILED")

    # Find the IPA file
    ipa_file = glob.glob("%s/**/*.ipa" % (build_dir), recursive=True)

    # Create zip file
    zipf = zipfile.ZipFile("%s/output.zip" % (build_dir), 'w', zipfile.ZIP_DEFLATED)
    zipf.write(ipa_file[0], basename(ipa_file[0]))
    zipf.close()

    # Upload the IPA file
    output_artifact_s3_location = job['data']['outputArtifacts'][0]['location']['s3Location']
    s3.upload_file("%s/output.zip" % (build_dir), output_artifact_s3_location['bucketName'], output_artifact_s3_location['objectKey'])


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
            try:
                print("Processing job: %s" % (job['id']))
                handle_job(job)
                cp.put_job_success_result(
                    jobId = job['id']
                )
            except:
                cp.put_job_failure_result(
                    jobId = job['id'],
                    failureDetails={
                        'type' : 'JobFailed',
                        'message' : 'BUILD FAILED'
                    }
                )
                traceback.print_exc(file=sys.stdout)
        
        time.sleep(SLEEP_TIME)

if __name__=="__main__":
    main()
