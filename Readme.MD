# Django Accounts Prototype

## Purpose

This project should be used as template to create a new Django application with the following features out of the box:

- User authentication & registration
- Forgot password functionality
- User Profile & change password

This should make setting up these features really easy to be able to start developing the actual main functionality of the application without having to build all of these features first.

The `CustomUser` model used in this authentication model is extending the `AbstractUser` and allows for quick & easy implementation of new user attributes and adding them to the admin page.

For details see [CustomUser model](#CustomUser-model)

## Pre-requisites

- Python3.x
- libjpeg-dev (image cropping)

    ```
    sudo apt-get install libjpeg-dev
    sudo apt-get install libjpeg8-dev
    ```
- redis-server (as service or Docer)
    ```
    # as service
    sudo apt install redis-server

    # via docker
    docker run -p 6379:6379 -d redis:latest
    
    # Check if redis is running
    redis-cli ping
    -> PONG

    ```


## Setup

- Fork the repository to a new repository
- Clone the newly forked repository onto your machine
- Create a new `.env` file in the `main` folder
<br>(This file will store your personal secrets for the emails server and s3 storage for static files. Make sure that the file is in the `.gitignore` file and is not pushed to the repo)

- Install the Python requirements
    ```
    pip install -r requirements.txt
    ```
- Run the migrations
    ```
    python manage.py migrate
    ``` 
- Collect static files
    ```
    python manage.py collectstatic
    ```
- Run the application and play around with it
    ```
    python manage.py runserver
    ```

## CustomUser model

Adding a new field to the `CustomUser` model is simple and very much the same as in any other Django model.

Simply add a new field in `accounts/models.py`


```
class CustomUser(AbstractUser):
    ...
    
    full_name = models.CharField(max_length=255)
```

To indicate that this is not a default field of `django.contrib.auth.models` assign it an `is_custom` attribute

```
class CustomUser(AbstractUser):
    ...
    
    full_name = models.CharField(max_length=255)
    full_name.is_custom = True
```

To assign it to a specific fieldset in the `UserChange` form a `fieldset` attribute can be assigned

```
full_name.fieldset = 'Personal info'
```

Other available attributes

```
# Add the field to the UserRegistration form
full_name.is_registration = True

# Add the field to the table display on the user admin page
full_name.is_list_display = True

# Add the field to the filter on the user admin page
full_name.is_list_filter = True

```

## Hosting Static and Media Files on AWS S3

In order to be able to use AWS S3 to host static and media files on AWS S3 storage you need to create an IAM user account and an S3 Storage bucket on AWS.

### Create a new IAM user

1) Go to https://console.aws.amazon.com/iam/home
2) Click on "Add user"
3) Enter a user name, select "Programmatic access" and click on "Next:Permissions"
4) Click on "Create group"
5) Enter a group name, search and select for the existing policy called "`AmazonS3FullAccess`" and click on "Create group"
6) Click on "Next:Tags" and again on "Next:Review"
7) Click on "Create User"
8) You will be shown the created user, the Access key ID and a hidden "Secret access key"
9) Click on "show" to display the "Secret access key" and copy all details to your `.env` file

### Create an S3 storage bucket

<b>IMPORTANT:</b> Don't store any confidential information in the S3 Storage bucket, this should only be used to serve static files

1) Go to https://s3.console.aws.amazon.com/s3/home
2) Click on "Create bucket"
3) Enter a (DNS-compliant) bucket name, select a region and (if you have any existing buckets) select to apply settings from an existing bucket
4) Configure options (if wanted) or click "Next"
5) Untick "Block all public access" (this is necessary in order for your files to be accessible on your website) and click on "Next"
6) Review your settings and click on "Create bucket" to finish
7) Copy the new bucket name and custom domain into your `.env` file


### Setting permissions for website access

Configure your storage bucket using the Bucket Policy file, CORS configuration
file and the Block Public Access screenshot in the the `deployment_configurations` folder 

<b>Further Reading:</b>

- [AWS's Setting permissions for website access](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteAccessPermissionsReqd.html)


## Adding an external SMTP server (e.g Sendgrid)

If you have your own SMTP server simpy add your details to the `.env` file.

If not create an email/SMTP account (e.g. Sendgrid, Gmail, etc) and add the details to your `.env` file.

Further Reading:
- [Sendgrid Single-Sender Verification](https://sendgrid.com/docs/ui/sending-email/sender-verification/)
- [Gmail Help IMAP/SMTP settings](https://support.google.com/mail/answer/7126229?hl=en)

## .env file

Your `.env` file should include the following details:

```
S3_USER=[IAM user account name]
AWS_ACCESS_KEY_ID=[IAM ACCESS KEY ID]
AWS_SECRET_ACCESS_KEY=[IAM SECRET ACCESS KEY]
AWS_STORAGE_BUCKET_NAME=[S3 Bucket Name]
AWS_S3_CUSTOM_DOMAIN=[S3 Bucket Name].s3.amazonaws.com
```
