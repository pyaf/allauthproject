#AllauthProject

A ready-made project for social logins with custom user model.

## Features

- Login with Facebook, Google+, Twitter.
- Custom User model.

## How to Use

To use this project, follow these steps:

1. Create your working environment.
2. Install requirements (`pip install -r requirements.txt`)
3. Runserver (`python manage.py runserver`)


## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate
