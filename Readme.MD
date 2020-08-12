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
    ` sudo apt-get install libjpeg-dev`

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