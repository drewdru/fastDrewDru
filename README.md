# fastDrewDru
backend for drewdru.com (https://github.com/drewdru/sitedrewdru)

## Manage progect
### Run project
#### Dev
```bash
python manage.py run
```
#### Prod
```bash
python manage.py run --prod
```
### Add new microservice
```bash
python manage.py startapp microservice_name [--prod]
```
### Run migrations commands
```bash
python manage.py migrations -h [--prod]
python manage.py migrations revision --autogenerate -m "Autogenerate migrations" [--prod]
```

## Deployment
