# WebSite
A website for a completely classic school class coded in django-nginx 

# Table of contents
1. [Introduction](#introduction)
2. [Django installation](#Django)
3. [Nginx installation](#Nginx)
4. [Usefull Additions](#Additions)
5. [Complements : le Siphoneur](#Siphoneur)

## Introduction <a name="introduction"></a>
The purpose of this repository is to help anyone create a website. In my case, I created a website for my class during my first year of preparatory class for the "grandes écoles", this class is called HX2. Hope this tutorial and my code helps you out, and if you have any questions or issues please feel free to contact me.

This whole tutorial was done with hx2 as the site name, so if you want to change it adapt the set of files provided accordingly. 

The structure of the site is simple: a home page (which in my case brings together school subjects), a presentation page of these sections with sub-sections, and finally a sub-sections page presenting the documents grouped by topic.

The administration pages reflect the same structure, and I added a custom filter for easier access to each subsection and documents (all this is discribe after)

We will first see how to configure the site backend with django and then we will see how to configure nginx for the site frontend. 

## Django Installation <a name="Django"></a>
__1. Depedencies__

Installation of necessary packages 
```
pip3 install django 
pip3 install bootstrap4
pip3 install mysqlclient 
pip3 install django-widget-tweaks 
pip3 install django-cleanup
```

__2. Set up django__
Place the folder hx2 in the right directory

For the ubuntu 20 users, create a user "www-data" and a group "www-data" with the appropriate permissions

__The in the settings file__
   * change your secret key and put yours
```python
SECRET_KEY = 'YOUR_SECRET_KEY'
```
   * change allowed hosts
```python
ALLOWED_HOSTS = ['127.0.0.1', 'website.com']
```
   * Change the database and put the right information (create a database and a user dedicated to django )
```python
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hx2DB',
        'USER': 'hx2User',
        'PASSWORD' : 'VivelaHX2!',
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}
```

   * Change your language
```python
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```


__2. Set up gunicorn__
Edit the file ```gunicorn_start.sh```
* Put your own name
```python
NAME="hx2Site"                              #Name of the application (*)
```

* Adapt the two following line with your right absolut path
```python
DJANGODIR=/var/www/hx2/hx2Site/            # Django project directory (*)
SOCKFILE=/var/www/hx2/run/gunicorn.sock        # we will communicate using this unix socket (*)

```

* Adapt the usernam and the group name if you didn't create the same user as me (www-data)
```python
USER=www-data                                        # the user to run as (*)
GROUP=www-data                                     # the group to run as (*)
```
Save and exit the file

Copy the file ```gunicorn_hx2Site.service``` in ```/etc/systemd/system/```

Run the command ```service gunicorn_hx2Site start```

## Nginx <a name="Nginx"></a>

## Useful additions  <a name="Additions"></a>

## Complements : le Siphoneur <a name="Siphoneur"></a>
