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

2. Create an iOS App using Xcode or use the provided sample in the sample_app/ directory.  If you do create a new app or use an existing one, be sure to copy the sample_app/Makefile and sample_app/exportOptions.plist.template to top-level of your project.

3. Run the Xcode builder script
```
python3 xcode_builder/builder.py
```

4. Open the ios-pipeline-example CloudFormation stack and find the CodeCommit repository.  Configure your iOS app to use the CodeCommit repository as a remote by either cloning it or adding it as a remote repository.

5. Checkin the code and push the changes to the CodeCommit repository.

6. Open the CodePipeline pipeline built using CloudFormation.  You should see the pipeline execute.  The Python script should also execute when the pipeline gets to the build stage.  Finally, the DeviceFarm test will run using the packaged app.
