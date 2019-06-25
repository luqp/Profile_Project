# Profile_Project
This project use Django to build a website where to display information of a user as a profile

## To use
You need create a new Python virtual environment:
```
python3 -m venv env
```
### Activate your new virtual Python environment
```
source ./env/bin/activate
```
If using Windows:
```
.\env\Scripts\activate
```
## Requirements
This project use some requirements located on requirements.txt file:
```
pip3 install -r requirements.txt
```

## Run app
To run the application you need to enter the catalog folder and run the server as follows:
```
(env) ...\Profile_Project> cd .\user_profile\
(env) ...\Profile_Project\user_profile> python manage.py migrate
(env) ...\Profile_Project\user_profile> python manage.py runserver
```
To see the webpage you have to make `ctrl + click` in `http://127.0.0.1:8000/`this open a new window in your browser
```
...
Django version 2.2.2, using settings 'user_profile.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

# Profile
<p align="center">
  <img src="https://github.com/windyludev/Profile_Project/blob/master/user_profile/media/images/profile.jpg">
</p>

## User
The project customs the user with `django.contrib.admin`. See the [link](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#custom-users-and-django-contrib-admin)

## Forms
The project overwrite some forms like `PasswordChangeForm` and `UserCreationForm`, and add a new one to show the user detail

## Password Validations
To validate the password the project setup the `settings.py`like the following:
```Python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('first_name', 'last_name'),
            'max_similarity': 0.3,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 14,
        }
    },
    {
        'NAME': 'accounts.validator.validators.UppercaseValidator',
    },
    {
        'NAME': 'accounts.validator.validators.LowercaseValidator',
    },
    {
        'NAME': 'accounts.validator.validators.SymbolValidator',
    },
]
```
Custom validations were defined in the folder `user_profile\accounts\validator\`
