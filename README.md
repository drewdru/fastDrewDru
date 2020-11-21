# fastDrewDru
Backend for personal website(drewdru.com) and fun


## Microservices
Frontend repository: https://github.com/drewdru/sitedrewdru


## Dependencies
1. Python >= 3.8.0
2. [requiremets.txt](requiremets.txt)
3. PostgreSql
4. Redis
5. Nginx


## Local Deployment
### Configure project
Create and configure .env file:
```bash
cp .env.example .env && cp .env.example .env.test && cp .env.example .env.ci
# if you use Docker: && cp .env.example .env.docker
```
To get a string for SECRET_KEY run:
```bash
openssl rand -hex 32
```
### Build dependencies
```bash
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
```
### Migrate
```bash
python manage.py migrations upgrade head
```


## Manage progect
### Run project
```bash
python manage.py run [--prod]
```
### Run tests
```bash
python manage.py test
```
### Add new microservice
```bash
python manage.py startapp microservice_name
```
### Run migrations commands
```bash
python manage.py migrations -h [--prod]
# Autogenerate migrations
python manage.py migrations revision --autogenerate -m "Autogenerate migrations" [--prod]
```

## Deployment
### Change enviromet variables in .env.prod
```bash
cp .env.example .env.prod && cp .env.example .env.test
```
### Build dependencies
```bash
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
```
### Migrate
```bash
python manage.py migrations upgrade head
```
### Add and run systemd service
```bash
sudo cp etc/fastDrewDru.service /etc/systemd/system/fastDrewDru.service
sudo systemctl daemon-reload
sudo systemctl start fastDrewDru # use restart on deploy
```
