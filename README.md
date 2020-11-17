# fastDrewDru
backend for drewdru.com (https://github.com/drewdru/sitedrewdru)

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
### Change enviromet variables
```bash
cp .env.dev .env && cp .env.dev .env.prod && cp .env.dev .env.test
```
