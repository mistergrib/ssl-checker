# This is a simple SSL certificate expiration reminder. 

You provide a list of the sites to the .env file, specify telegram bot token, chat ID and the amount of days before certificate expiration.
You can enable or disable type of notifications (telegram and/or email)

## .env file example:
```
# here the list of sites for which you want to check ssl certificate
HOSTNAMES=google.com,youtube.com,facebook.com,wikipedia.org
# DAYS_THRESHOLD specify the amount of days before certificate will expired
DAYS_THRESHOLD=5

# Enable alerts via telegram
TELEGRAM_ALERTS_ENABLED=true
BOT_TOKEN=1111111111:AAA-P33ey64560GRfgre-tvp45r2Isgf4I6HD0
CHAT_ID=-999999999

# Enable alerts via email SMTP server
EMAIL_ALERTS_ENABLED=true
# Email SMTP setting
SMTP_SERVER=mail.test.test
SMTP_PORT=587
# you should choose one of the SMTP_STARTTLS_ENABLED or SMTP_SSL_ENABLED
# SMTP_STARTTLS_ENABLED can be True or False if you using STARTTLS (587 port by defauld)
# SMTP_SSL_ENABLED can be True or False if you using SSL (465 port by default)
SMTP_STARTTLS_ENABLED=true
SMTP_SSL_ENABLED=false

EMAIL_LOGIN=ssl_checker@test.test
EMAIL_FROM_ADDRESSES=ssl_checker@test.test
EMAIL_PASSWORD=12345
EMAIL_SUBJECT="SSL Checker notifies:"
EMAIL_RECIPIENT=ssl_alerts@test.test,admin@test.test
```

## usage:
You should create .env file as described above

```
docker pull mistergrib/ssl_checker:latest
docker run --env-file .env --name ssl_checker -d mistergrib/ssl_checker:latest
```

The script runs once, after which the container stops.
To run it again you can just start the container with simple command
```
docker container start ssl_checker
```

## cron file example
You can schedule it with cron, the following example runs the script every day at 12:00
```
0 12 * * * /usr/bin/docker container start ssl_checker >> /var/log/ssl_checker_cron.log 2>&1
```
