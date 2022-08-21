# Installation

## The portal itself

1) Execute `mkdir <DIRECTORY>`, this will create directory where repo contents will be cloned to.
2) Execute `cd <DIRECTORY>`
3) Clone the repository.
4) Upgrade pip to latest version by executing `pip install --upgrade pip`
5) Execute `apt-get install libpq-dev`
6) Execute `pip install -r requirements.txt`
7) Set credentials in `projects/settings.py`.
8) Apply migrations by executing `python3 manage.py makemigrations` first, and then execute `python3 manage.py migrate`

## Background video upload service

1) Copy `config/systemd/upload-videos-background.service` to `/etc/systemd/system/upload-videos-background.service`
2) In `/etc/systemd/system/upload-videos-background.service`, set user,from which background video upload service will be running, and directory, where the Django's project `manage.py` file is located (denoted as USER and PORTAL_DIR respectively).
3) Execute `sudo systemctl enable upload-videos-background.service`
4) Execute `sudo systemctl start upload-videos-background.service`

*It is recommended that before adding to systemctl you first run the service manually to ensure that no errors occur.*

## Nginx - deny access to mp4 files

1) Copy location denial rule from `config/nginx.conf.dist` to your nginx config (usually placed at `/etc/nginx/nginx.conf`).
2) Check for syntax errors by executing `nginx -t`
3) If no errors occured on previous step, restart nginx to apply the changes - execute `sudo systemctl restart nginx`
