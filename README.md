# smart-classroom-ceph-openfaas

## **Team Details** 

**Team name:** BlankSPace

**Group members:**

- Anisha Das
- Piyush Garg
- Kashish Khullar

## **Member Responsibilities**

**Piyush:** 
- Efficiently executed the tasks of setting up the OpenFaas and configured it to run on Virtual Machine
- Migrated the Openstack from virtualbox to an AWS EC2 instance for better performance.
- Built a customized Docker image containing essential libraries and tools, updated the dockerfile to refer to the correct encoding and handler file.
- Deployed the dockerfile Docker Hub for secure image storage of the docker image
- Deployed the serverless function using the Docker image to OpenFaas.
- Collaborated with the team to execute end to end testing and report creation.


**Anisha:**

- Efficiently executed the tasks of setting up the Ceph and configured it to run on Virtual Machine
- Proceeded to set up Ceph buckets as well as the permissions on the serverless function for bucket access.
- Setup the DynamoDB table, populated the table with the provided student data JSON using Python script.
- Configured the serverless function trigger on the input bucket to enable automatic execution of the serverless function upon receiving new files using a polling mechanism.
- Debugged and set the permissions and configurations of the serverless function for successful execution.
- Updated the workload generator code to efficiently visualize the output, by adding functions to fetch the contents of the output S3 bucket and display the contents of the CSV files.
- Identified and resolved various issues during testing, such as resolution of the permission error for user on the bucket, OSD mounting etc
- Collaborated with the team to execute end to end testing and report creation


**Kashish:**

- Implemented the handler code to process video files.
- Fine tuned serverless function infra configurations and code to make it available and reduce spin-up time.
- Integrated the Python face recognition library, enabling accurate identification of individuals in the extracted frames.
- Developed code to generate output CSV files containing student information derived from the face recognition process.
- Tested the serverless function using the provided workload generator to evaluate its performance and reliability under simulated real-world scenarios.
- Verified the correctness of the output CSV files and assessed processing times to ensure all requests were completed within a reasonable timeframe.
- Created the project report and the architectural diagram


## **AWS Credentials** 

No specific AWS credentials are required for running this application. The workload generator has been hardcoded with the input and output bucket names. Running the workload genetor itself is enough.

## **S3 Buckets**   

- ceph-bkt-input-blankspace
- ceph-bkt-output-blankspace

## **Other AWS resources used**   

- OpenFaas Function --> face_recognition
- DynamoDB table --> blankSpace-student-data

## **Description**

This project integrates OpenFaas, Ceph, and AWS to monitor Ceph input, process videos with a serverless function, and retrieve academic info using face recognition and DynamoDB. It demonstrates a flexible application architecture and precise controls via a private cloud, reducing reliance on third-party vendors. OpenFaas enables serverless computing and networking solutions, deploying functions via Docker without dedicated servers. Leveraging Ceph for storage and AWS DynamoDB for data search, it simplifies deployment with lightweight Docker images, tailored for Platform as a Service (PaaS) users' specific needs.
