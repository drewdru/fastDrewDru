#!/bin/bash
case $1 in
  dev)
    cd /home/drewdru/develop/python/backendDrewdru/
    source env/bin/activate
    python manage.py migrations upgrade head
    python manage.py run
    ;;
  prod)
    cd /home/drewdru/develop/python/backendDrewdru/
    source env/bin/activate
    python manage.py migrations upgrade head --prod
    python manage.py run --prod
    ;;
  docker)
    python manage.py migrations upgrade head --docker
    python manage.py run --docker
    ;;
esac
