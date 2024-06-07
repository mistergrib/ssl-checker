# This is a simple SSL certificate expiration reminder. 

You provide a list of the sites to the .env file, specify telegram bot token, chat ID and the amount of days before certificate expiration.

## .env file example:
```
HOSTNAMES=google.com,youtube.com,facebook.com,wikipedia.org
BOT_TOKEN=1111111111:AAA-P33ey64560GRfgre-tvp45r2Isgf4I6HD0
CHAT_ID=-999999999
DAYS_THRESHOLD=100
```

## usage:
You should create .env file as described above

```
docker pull mistergrib/ssl_checker:v1.0
docker run --env-file .env --name ssl_checker -d mistergrib/ssl_checker:v1.0
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
