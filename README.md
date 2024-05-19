
# SSO Authentication for multi-application hosted in multi clouds
This project proposes a solution for Single Sign-On (SSO) authentication tailored for multi-application environments hosted across diverse cloud providers. Leveraging JSON Web Tokens (JWT) for authentication, our approach stores tokens within cookies for efficient management and persistence. We ensure seamless user access while prioritizing security through SSL (Secure Sockets Layer) encryption to protect cookie transmission for data integrity. Additionally, our system employs authorization binding using Role-Based Access Control (RBAC) to manage user roles and permissions centrally, enhancing the security and granularity of access control across applications.



## Run Locally
This part using the code in localhost folder to run our system in localhost. You can follow these steps below to Start our system.

Clone the project:

```bash
  git clone https://github.com/Peerawichaya27/SSO_Cookies-JWT
```

Go to the project directory:

```bash
  cd localhost
```

Install dependencies:

```bash
  pip install --upgrade -r requirements.txt
```

Start the server:

```bash
  python <APP-NAME.py>
```


## Deploy AWS Elastic Beanstalk (authentication_service2)
This part using the code in deploy\aws folder to run our authentication_service2 in AWS Elastic Beanstalk. You can follow these steps below to deploy our system.

Clone the project:

```bash
  git clone https://github.com/Peerawichaya27/SSO_Cookies-JWT
```

Go to the project directory:

```bash
  cd deploy\aws\authentication_service2
```
Initialize your EB CLI repository:

```bash
  eb init
```

Deploy your application:

```bash
  eb deploy
```
Open your application on your browser:

```bash
  eb open
```


## Deploy to AWS App Runner (Application3)
This part using the code in deploy\aws folder to run our Application3 in AWS App Runner. You can follow these steps below to deploy our system.

Clone the project:

```bash
  git clone https://github.com/Peerawichaya27/SSO_Cookies-JWT
```

Go to the project directory:

```bash
  cd deploy\aws\application3
```
Build the Docker image:

```bash
  docker build -t app3 .
```

Create a repository on ECR:

```bash
   aws ecr create-repository --repository-name flask-apprunner
```
Tag the Docker image with the URI of the repository we just created:

```bash
  aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```
Login to your AWS and Docker to tag the Docker image the repository we just created:

```bash
  aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```
Tag the Docker image with the URI of the repository we just created:

```bash
  docker tag flask-apprunner-img:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/flask-apprunner:latest
```
push the Docker image to Amazon ECR:

```bash
  docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/flask-apprunner:latest
```
Then we just create sevice from AWS app runner by using ECR repository in aws platform.
## Deploy to Google Cloud Run (Application1, Application2, Authentication_Service1, SSO_service)
This part using the code in deploy\Google_Cloud folder to run our Application1, Application2, Authentication_Service1 and SSO_service in Google Cloud Run. You can follow these steps below to deploy our system.

Clone the project:

```bash
  git clone https://github.com/Peerawichaya27/SSO_Cookies-JWT
```

Go to the project directory:

```bash
  cd deploy\Google_Cloud\<APP-NAME>
```
Initialize the gcloud CLI:

```bash
  gcloud init
```

Set the default project for your Cloud Run service:

```bash
   gcloud config set project <PROJECT_ID>
```

In your source code directory, deploy from source:

```bash
   gcloud run deploy
```
## Running Tests
This part using the code in Test folder to test our system. We also include tradional sso system code in this folder, you can use thees code to compare the performance with our system by deploy it to Google Cloud Run by using steps above. You can follow these steps below to run the test for our system.

Clone the project:

```bash
  git clone https://github.com/Peerawichaya27/SSO_Cookies-JWT
```

Go to the test directory:

```bash
  cd test
```

Start the test:

```bash
  python <TEST-NAME.py>
```