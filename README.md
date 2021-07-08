# WebSite
A website for a completely classic school class coded in django-nginx-mysql

# Table of contents
1. [Introduction](#introduction)
2. [Mysql Set Up](#Mysql)
3. [Django Set Up](#Django)
4. [Nginx Set Up](#Nginx)
5. [Usefull Additions](#Additions)
6. [Complements : the Siphoneur](#Siphoneur)

## Introduction <a name="introduction"></a>
The purpose of this repository is to help anyone create a website. In my case, I created a website for my class during my first year of preparatory class for the "grandes écoles", this class is called HX2. Hope this tutorial and my code helps you out, and if you have any questions or issues please feel free to contact me.

This whole tutorial was done with hx2 as the site name, so if you want to change it adapt the set of files provided accordingly. The server used was an ubuntu 20.04.

The structure of the site is simple: a home page (which in my case brings together school subjects), a presentation page of these sections with sub-sections, and finally a sub-sections page presenting the documents grouped by topic.

The administration pages reflect the same structure, and I added a custom filter for easier access to each subsection and documents (all this is discribe after)

There is a compartmentalization of users and files. Each file therefore belongs to a section which is attached to a compartment called here "Année". For a user to have access to this file, he must belong to a group with the same name as this "Année". A user can belong to several groups, so he can have access to several years. Finally, in my case, I had created 3 types of users, the Administrator with all the rights (in dango you can run the command ```python3 manage.py createsuperuser```), a user having only the right to consult the documents (you simply have to remove the access rights to the administrator interface, and give no permission) and a moderating user who had the right to access the administrator interface with the corresponding permissions and who could add files or sub-sections in the "Years" to which he belongs. 

Moreover, the management of the media is pretty simple, in the directory ```media``` there are two others subdirectories ```fichiersdeposes``` and ```static```.
* In ```static```, there are all the files necessary for the proper functioning of the site: style files and javascript files. (You can add your staticfiles with the command ```python3 manage.py collectstatic``` ). You can also put files used by your website that do not require the user to be logged in, for example your website logo. 
* In ```fichiersdeposes``` there are all the uploaded files (as the French name suggests). These files are accessible by following the partitioning explained previously. There is also a subdirectory ```permanent```. In this subdirectory you put all the files used by your website but which requires the user to be at least logged in. 

We will first see how to configure the site backend with django and then we will see how to configure nginx for the site frontend. 

## Mysql Set Up <a name="Mysql"></a>
If you don't want to set up mysql skip this section and adapt the settings file as explain after.

### 1. Mysql Installation

Install Mysql
```
sudo apt install mysql-server
```

Run the security script 
```
sudo mysql_secure_installation
```

Access to mysql
```
sudo mysql
```

Create the user that will be used by django and its password :
```sql
CREATE USER 'djangoUser'@'localhost' IDENTIFIED BY 'password';
```

Create the database that django will used by django
```sql
CREATE DATABASE djangoDB;
```

And give him the privilegies
```sql
GRANT ALL PRIVILEGES ON djangoDB.* TO 'djangoUser'@'localhost';
FLUSH PRIVILEGES;
```
And your database is ready, all you have to do now is allow python to have access to it.

### 2. Connect python to mysql

Install pip if you don't have it :
```
sudo apt install python3-pip
```

Install the package
```
pip3 install mysqlclient
```

If you have an error like me, you may be missing these two packages: 
```
sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev
```

## Django Set Up <a name="Django"></a>
### 1. Depedencies

Installation of necessary packages 
```
pip3 install django 
pip3 install bootstrap4
pip3 install django-widget-tweaks 
pip3 install django-cleanup
```

### 2. Django Set Up

Place the folder hx2 in the right directory (personally I placed it in ```/opt/``` )

For the ubuntu 20 users, create a user "www-data" and a group "www-data" with the appropriate permissions

__The in the settings file__
   * change your secret key and put yours
```python
SECRET_KEY = 'YOUR_SECRET_KEY'
```

You can generate one with (in ```python3 manage.py shell```) :
```python
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
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
        'NAME': 'djangoDB',
        'USER': 'djangoUser',
        'PASSWORD' : 'password!',
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

See if everything is working by doing: 
```
python3 manage.py makemigrations
python3 manage.py migrate
```

(And if you don't have the right permissions, you can use  ```sudo chown -R www-data:www-data ./migrations```)

And create a super user
```
python3 manage.py createsuperuser
```

### 3. Gunicorn Set Up
Install it
```
pip3 install gunicorn
sudo apt-get install gunicorn
```

Edit the file ```gunicorn_start.sh```
* Put your own name
```python
NAME="hx2Site"                              #Name of the application (*)
```

* Adapt the two following line with your right absolut path
```python
DJANGODIR=/opt/hx2/hx2Site/            # Django project directory (*)
SOCKFILE=/opt/hx2/run/gunicorn.sock        # we will communicate using this unix socket (*)

```

* Adapt the usernam and the group name if you didn't create the same user as me (www-data)
```python
USER=www-data                                        # the user to run as (*)
GROUP=www-data                                     # the group to run as (*)
```
Save and exit the file

In the file ```gunicorn_hx2Site.service```, modify this lines so that it suits you:
```
Environment="LANG=fr_FR.UTF-8,LC_ALL=fr_FR.UTF-8"
User=www-data
ExecStart=/opt/hx2/gunicorn_start.sh
```

Copy the file ```gunicorn_hx2Site.service``` in ```/etc/systemd/system/```
```
sudo cp gunicorn_hx2Site.service /etc/systemd/system/
```

Run the command ```service gunicorn_hx2Site start```

And normally you have finished installing your django server, it is operational. You can join it on the port 8000 in localhost or on your local network if you opened this port.

## Nginx Set Up <a name="Nginx"></a>

### 1. Let's Encrypt Set Up with OVH for ssl securisation
(this part of the tutorial is largely inspired by https://buzut.net/certbot-challenge-dns-ovh-wildcard/ )

Install dependecies
```python
pip3 install certbot 
pip3 install certbot-dns-ovh
```

Create the config file at ```/etc/logrotate.d/cerbot``` with:
```
/var/log/letsencrypt/*.log {
        monthly
        rotate 6
        compress
        delaycompress
        notifempty
        missingok
        create 640 root adm
}
```

Create the API. In the following command replace ```{domain.ext}``` by your domain and becareful it is the the root domain name .
(You may need to install this package: ```sudo apt install libwww-perl```) 
```
GET /domain/zone/
GET /domain/zone/{domain.name}/
GET /domain/zone/{domain.ext}/status
GET /domain/zone/{domain.ext}/record
GET /domain/zone/{domain.ext}/record/*
POST /domain/zone/{domain.ext}/record
POST /domain/zone/{domain.ext}/refresh
DELETE /domain/zone/{domain.ext}/record/*
```
If this is too restrictive for you, you may prefer these commands: 
```
GET /domain/zone/*
PUT /domain/zone/*
POST /domain/zone/*
DELETE /domain/zone/*
```

Connect to https://api.ovh.com/createToken/ to get the rigth information access for your API

Create ```/root/.ovhapi``` and add:
```
dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = YOUR_APPLICATION_KEY
dns_ovh_application_secret = YOUR_SECRET
dns_ovh_consumer_key = YOUR_PERSONAL_KEY
```

```
chmod 600 /etc/certs/.ovhapi
```

Generate the certificate for your ```website.com``` and ```*.website.com```, they are two separate certificates but they will be put in the same file.
```
sudo certbot certonly --dns-ovh --dns-ovh-credentials /etc/certs/.ovhapi -d website.com -d *.website.com
```

You can do in several steps to get the two certifiactes in two different files with 
```
certbot certonly --dns-ovh --dns-ovh-credentials ~/.ovhapi -d *.website.com
```
Or make it automatically with no interaction with
```
certbot certonly --dns-ovh --dns-ovh-credentials ~/.ovhapi --non-interactive --agree-tos --email mon@email.fr -d website.com -d *.website.com
```

Then
```
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

When the certificates will expire run ```certbot renew``` to genrate new ones, but this is probably not compatible with the DNS plugins that we have just set up.
Thus you can make a small script to automate this, put in ```/usr/local/sbin/renewCerts.sh```
```
#!/bin/bash

/usr/local/bin/certbot certonly --dns-ovh --dns-ovh-credentials /root/.ovhapi --non-interactive --agree-tos --email mon@email.fr -d website.com
/usr/local/bin/certbot certonly --dns-ovh --dns-ovh-credentials /root/.ovhapi --non-interactive --agree-tos --email mon@email.fr -d *.website.com
```

You can then call it once a month with a crontab and you can be sure that you have always up-to-date certificates. 
```
22 4 5 * * /usr/local/sbin/renewCerts.sh > /dev/null 2>&1
```

Voila, your ssl certificate is ready.

### 2. Nginx Installation

```
sudo apt-get update
sudo apt-get -y install nginx

sudo service nginx restart
```
In my Nginx file, change :
```
hx2.tlapp.net www.hx2.fr hx2.fr
/var/www/hx2/hx2Site/media/static/
/var/www/hx2/hx2Site/media/fichiersdeposes/

ssl_certificate /etc/letsencrypt/live/website.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/website.com/privkey.pem;

ssl_trusted_certificate /etc/letsencrypt/live/website.com/chain.pem;
```

Put my nginx file in ```/etc/nginx/sites-available/website.com``` and make 
```sudo ln -s /etc/nginx/sites-available/website.com /etc/nginx/sites-enabled/```

Finally
```sudo systemctl restart nginx```

NB : 
* ```/etc/nginx/nginx.conf``` is the main configuration file, you can modify its properties to suit your requirements 
* ```/var/log/nginx/access.log``` Nginx save all the access demand
* ```/var/log/nginx/error.log``` is the file where Nginx save all the errors

To check if a certificate is correct you can use "Online Certificate Status Protoocl (OCSP)"
Run ```openssl s_client -connect website.com:443 -tls1_2 -tlsextdebug -status | grep "OCSP Response Status: successful" ```
And ```openssl s_client -showcerts -connect website.com:443 -tls1_2 -tlsextdebug -status | grep "OCS" ```

## Useful Additions  <a name="Additions"></a>

Explains tamplatags, templates base, dictioary, the document access system  ...

__ Useful commands __ 
* ```python python3 manage.py runserver``` with ```0.0.0.0``` to listen on all interface, ```--insecure``` (but dangerous)
* ```python python3 manage.py makemigrations``` and ```python python3 manage.py migrate```
* ```python python3 manage.py shell```
* ```python python3 manage.py runscript``` (but requires configurations so prefer the method that I use in "le siphoneur")
* ```python python3 manage.py flush``` to erase the database


## Complements : the Siphoneur <a name="Siphoneur"></a>

The "Siphoneur" aims to siphon a main directory with the same structure as the site and to put all the documents directly on the website automatically. 
Change the absolute path or remove the ```#``` to take the path as argument
```python
#walk_dir = sys.argv[1]
walk_dir = "/path/to/the/folder/to/siphon/"
```

Run the command

```python
python3 siphoneur.py
```
