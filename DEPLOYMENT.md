# Deployment Guide

## Production Deployment Guide for Meteor Madness Backend

### Prerequisites

-   Ubuntu 20.04+ or similar Linux distribution
-   Python 3.10+
-   PostgreSQL 14+
-   Redis 6+
-   Nginx
-   Supervisor (for process management)

## Step 1: Server Setup

### Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Dependencies

```bash
sudo apt install -y python3-pip python3-dev python3-venv
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y nginx
sudo apt install -y supervisor
sudo apt install -y libpq-dev
```

## Step 2: Database Setup

### Create PostgreSQL Database

```bash
sudo -u postgres psql

CREATE DATABASE meteor_madness;
CREATE USER meteor_user WITH PASSWORD 'your_secure_password';
ALTER ROLE meteor_user SET client_encoding TO 'utf8';
ALTER ROLE meteor_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE meteor_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE meteor_madness TO meteor_user;
\q
```

## Step 3: Application Setup

### Create Application User

```bash
sudo useradd -m -s /bin/bash meteorapp
sudo su - meteorapp
```

### Clone Repository

```bash
cd /home/meteorapp
git clone <your-repo-url> meteor-madness-backend
cd meteor-madness-backend
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### Configure Environment

```bash
cp .env.example .env
nano .env
```

Edit `.env` with production values:

```
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=meteor_madness
DB_USER=meteor_user
DB_PASSWORD=your_secure_password
NASA_API_KEY=your_nasa_api_key
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Create Logs Directory

```bash
mkdir -p /home/meteorapp/meteor-madness-backend/logs
```

## Step 4: Gunicorn Configuration

### Create Gunicorn Configuration

```bash
nano /home/meteorapp/meteor-madness-backend/gunicorn_config.py
```

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
errorlog = "/home/meteorapp/meteor-madness-backend/logs/gunicorn-error.log"
accesslog = "/home/meteorapp/meteor-madness-backend/logs/gunicorn-access.log"
loglevel = "info"
```

## Step 5: Supervisor Configuration

### Create Gunicorn Supervisor Config

```bash
sudo nano /etc/supervisor/conf.d/meteor-madness-gunicorn.conf
```

```ini
[program:meteor-madness-gunicorn]
directory=/home/meteorapp/meteor-madness-backend
command=/home/meteorapp/meteor-madness-backend/venv/bin/gunicorn meteor_madness.wsgi:application -c gunicorn_config.py
user=meteorapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/meteorapp/meteor-madness-backend/logs/gunicorn-supervisor.log
```

### Create Celery Worker Config

```bash
sudo nano /etc/supervisor/conf.d/meteor-madness-celery.conf
```

```ini
[program:meteor-madness-celery]
directory=/home/meteorapp/meteor-madness-backend
command=/home/meteorapp/meteor-madness-backend/venv/bin/celery -A meteor_madness worker -l info
user=meteorapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/meteorapp/meteor-madness-backend/logs/celery.log
```

### Create Celery Beat Config

```bash
sudo nano /etc/supervisor/conf.d/meteor-madness-celery-beat.conf
```

```ini
[program:meteor-madness-celery-beat]
directory=/home/meteorapp/meteor-madness-backend
command=/home/meteorapp/meteor-madness-backend/venv/bin/celery -A meteor_madness beat -l info
user=meteorapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/meteorapp/meteor-madness-backend/logs/celery-beat.log
```

### Update Supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

## Step 6: Nginx Configuration

### Create Nginx Config

```bash
sudo nano /etc/nginx/sites-available/meteor-madness
```

```nginx
upstream meteor_madness {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/meteorapp/meteor-madness-backend/staticfiles/;
    }

    location /media/ {
        alias /home/meteorapp/meteor-madness-backend/media/;
    }

    location / {
        proxy_pass http://meteor_madness;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /ws/ {
        proxy_pass http://meteor_madness;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/meteor-madness /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 7: SSL Configuration (Let's Encrypt)

### Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Obtain SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Auto-renewal

```bash
sudo certbot renew --dry-run
```

## Step 8: Redis Configuration

### Configure Redis

```bash
sudo nano /etc/redis/redis.conf
```

Set:

```
bind 127.0.0.1
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Restart Redis

```bash
sudo systemctl restart redis-server
sudo systemctl enable redis-server
```

## Step 9: Monitoring & Logging

### Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/meteor-madness
```

```
/home/meteorapp/meteor-madness-backend/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 meteorapp meteorapp
    sharedscripts
    postrotate
        supervisorctl restart meteor-madness-gunicorn
    endscript
}
```

## Step 10: Firewall Configuration

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Step 11: Initial Data Load

### Sync NEO Data

```bash
source venv/bin/activate
python manage.py shell
```

```python
from neos.services import NEODataService
service = NEODataService()
service.sync_neo_data()
exit()
```

## Maintenance Commands

### View Supervisor Status

```bash
sudo supervisorctl status
```

### Restart Services

```bash
sudo supervisorctl restart meteor-madness-gunicorn
sudo supervisorctl restart meteor-madness-celery
sudo supervisorctl restart meteor-madness-celery-beat
```

### View Logs

```bash
tail -f /home/meteorapp/meteor-madness-backend/logs/gunicorn-error.log
tail -f /home/meteorapp/meteor-madness-backend/logs/celery.log
```

### Update Application

```bash
cd /home/meteorapp/meteor-madness-backend
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart all
```

## Backup Strategy

### Database Backup

```bash
pg_dump -U meteor_user meteor_madness > backup_$(date +%Y%m%d).sql
```

### Automated Daily Backup (Cron)

```bash
crontab -e
```

Add:

```
0 2 * * * pg_dump -U meteor_user meteor_madness > /home/meteorapp/backups/db_$(date +\%Y\%m\%d).sql
```

## Performance Optimization

### PostgreSQL Tuning

```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```

Adjust based on your server:

```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 2621kB
min_wal_size = 1GB
max_wal_size = 4GB
```

### Redis Optimization

Adjust maxmemory based on your needs in `/etc/redis/redis.conf`

## Troubleshooting

### Check Service Status

```bash
sudo systemctl status nginx
sudo systemctl status redis-server
sudo systemctl status postgresql
sudo supervisorctl status
```

### View Application Logs

```bash
tail -f /home/meteorapp/meteor-madness-backend/logs/*.log
```

### Django Debug

```bash
python manage.py check
python manage.py check --deploy
```

## Security Checklist

-   [ ] DEBUG = False in production
-   [ ] Strong SECRET_KEY configured
-   [ ] Database password is secure
-   [ ] Firewall configured
-   [ ] SSL certificate installed
-   [ ] Regular backups scheduled
-   [ ] Log monitoring configured
-   [ ] Rate limiting enabled
-   [ ] CORS properly configured
-   [ ] Security headers configured

## Monitoring & Alerts

Consider setting up:

-   Sentry for error tracking
-   Prometheus + Grafana for metrics
-   UptimeRobot for uptime monitoring
-   Cloudflare for DDoS protection

Your Meteor Madness backend is now deployed! 🚀
