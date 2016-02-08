# Keystone for Python

## Overview

Developed with the [Django](https://www.djangoproject.com/) framework, with minimum setup to enable you to have basic user authentication, login with Facebook and getting access token.

## Setup

* Make sure you have [Python](https://www.python.org/)
* Install [virtualenv](https://virtualenv.readthedocs.org/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/)
* Download this project and use `mkvirtualenv -a path/to/it project_name` to create the project
* In `/your_python_env/project_name/bin/postactivate`, make sure you define these environment variables:
  * `export FACEBOOK_APP_ID="<your_app_id>"`
  * `export FACEBOOK_APP_SECRET="<your_app_secret>"`
  * `export SECRET_KEY="<secret_key_for_django>"`
* `workon project_name`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runsslserver`

Go to the site, register a new user, then go to the login page to login with Facebook.

From there return to the main page you can see that your Facebook user is logged in and the access token is stored in the user.

Check the home view in `/keystone/common/views.py` for how to use this user session and the associated access token.

Enjoy!
