### Trim-Be
----
REST API backend of the Trim application written in Flask-Restful. View the live application [here](https://trimm.xyz "here").

The front end is written in Angular and can be found [here](https://github.com/olamileke/trim-fe "here").

To run this application locally, you need to have python3+ on your system. Get it 
[here](https://https://www.python.org/downloads/ "here"). Make sure to add python.exe to your operating system path variables to be able to run python scripts from the command line.

Navigate into a directory of choice on your system and run
``` 
git clone -b clone --single-branch https://github.com/olamileke/trim-be.git
```
This will clone the clone(sorry, double entendre!) branch onto your system. The clone branch contains the scrubbed configuration.py file into which you will enter relevant application secrets.

Navigate into the application root by running
```
cd Trim-be
```

At this point, we need to create the virtual machine in which the application will run. Depending on if you are working in a windows or linux environment, follow the instructions found [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/ "here") to create the virtual environment.

Activate the virtual environment by running 
```
venv\scripts\activate
```
or 
```
source venv/scripts/activate
```
for windows and linux respectively.  Now, with the virtual environment active, run the following command
```
pip install -r requirements.txt
```
This will install all the application dependences as outlined in the requirements.txt file in the app root.

There are also several other components needed for the application to run. These are

- AWS access credentials.  [Create](https://portal.aws.amazon.com/billing/signup "Create") an AWS account and add your credit card to enable you make use of the free tier or if you have cash(baller!) make use of the paid tier. 

  Create an IAM user and take note of the unique access key id and the secret access key. This is especially important as you will not be able to view it again.

  Finally, enable S3 permissions for this IAM user. If there are any issues, check out this [guide](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/setting_up_create_iam_user.html  "guide").

- An S3 bucket. Log into the [S3 console](https://console.aws.amazon.com/s3/home "S3 console") and create a new S3 bucket.  Note the *bucket name* and the *region* in the name and region tab. Make sure to untick the *block public options* in the set permissions tab. This is needed to make sure that you can access objects in the bucket from the application.

- An Amazon RDS Postgresql database instance.  Follow the instructions found [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html "here") to get your instance set up. Take note that by default, the name of your database will be *postgres*. Make sure to edit the default security rules to ensure to ensure that the instance is set up to accept inboundtraffic from anywhere via TCP/IP on port 5432, the default port. 

  An alternative Postgresql cloud service provider is [elephantsql](https://www.elephantsql.com/ "elephantsql"). Read their documentation to set up the postgres database. In my experience though, I have found Amazon RDS to be faster than elephantsql, plus elepantsql is a bit more limited.
  
- Mailgun credentials to enable the sending of mails in the app. [Create](https://signup.mailgun.com/new/signup "Create") a mailgun account and [login](https://login.mailgun.com/login/ "login") to your mailgun dashboard.

  Seeing as the application will be running locally/is not live, you need to create a sandbox domain for testing mail functionality locally. Do that [here](https://app.mailgun.com/app/sending/domains "here"). 

  Take note of the domain name with the *sandbox prefix* and the *private api key* for the domain. Find the api key [here](https://app.mailgun.com/app/sending/domains  "here"). For sandbox domains, you need to verify an email address or addresses you have access to for the domain.

  This are the only email(s) you will be able to send mails to from the app making use of the sandbox domain. Do this from the created sandbox domain tab.

Locate the configuration.py file in the application root and do the following

- Set DB_USER to the username of the postgresql database instance
- Set DB_PASSWORD to the password of the postgresql database instance
- Set DB_PORT to the endpoint obtained from AWS RDS
- Set DB_NAME to the name of the database. For AWS RDS, by default it is *postgres* while for elephantsql set it to whatever name is set.
- Set SECRET_KET to any unique random string of at least 10 characters. Check out tools on the internet like this [one](https://www.random.org/strings/ "one") for generating random strings
- Set CLIENT_URL to whatever localhost url the cloned frontend is running on
- Set MAIL_BASE_URL to the mailgun sandbox domaun you created earlier for testing
- Set MAIL_API-KEY to the private api key of your mailgun account. This api key has a *key -* prefix
- Set MAIL_FROM to *trim* or whatever name you desire
- Set MAIL_FROM_URL to *support@trim.test* or whatever url you desire
- Set S3_BUCKET to the name of the s3 bucket you created earlier
- Set S3_BUCKET_LINK to https://s3-**aws-region**.amazonaws.com/**bucket-name**/ with aws-region being the region of the S3 bucket and bucket-name being the name of the bucket. Make sure to remove the asterisks(****)
- Set S3_ACCESS_KEY_ID to the access key id of the IAM(AWS) user created earlier
- Set S3_SECRET_KEY to the secret access key of the IAM(AWS) user created earlier

The next step is to set up the database. Run
```
python manage.py db init
```
This creates the migrations folder in which database migrations will be stored. Then run
```
python manage.py db migrate -m 'create database schema'
```
This creates a single migration based on the */models.py* file located in the application root which defines all the database tables and the various relationships between them. Then, run
```
python manage.py db upgrade
```
This runs the just created migration on the database and creates all the tables and relationships. To roll back this migration, run
```
python manage.py db downgrade
```
To view all the data contained in the database, make use of a client like [PGAdmin](https://www.pgadmin.org/ "PGAdmin")

Finally, run the following command to start the application
```
python app.py
```
Here, the application will be available at http://localhost:5000
