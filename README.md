# Continuous Integration and Continuous Delivery for iOS Apps

This repository contains code to build out a CI/CD pipeline for iOS apps.  The pipeline is built using AWS CodePipeline with AWS CodeCommit as the source repository.  The compilation, packaging and signing of the iOS app is done using a machine running macOS with Xcode as a CodePipeline Custom Action.  The xcode_builder/ directory contains a Python script which will poll CodePipeline for jobs and once it gets it, it will retrieve the source artifact, perform the build and deliver the built artifact back to CodePipeline.  The testing is performed using AWS DeviceFarm.

## Contents
- sample_app/
- xcode_builder/
- pipeline.yaml

## Usage

1. Create the CodeCommit repository, pipeline, and DeviceFarm project using the provided CloudFormation template:
```
aws cloudformation deploy --stack-name ios-pipeline-example --template-file pipeline.yaml --capabilities CAPABILITY_IAM
```

