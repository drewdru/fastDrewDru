#!/usr/bin/env bash

args=("$@")

case "${1}" in
    "build")
        docker build -t fast_drew_dru:latest -f Dockerfile .
        ;;
    # region db
    "run-db")
        docker run \
            -v $(pwd)/data:/docker-entrypoint-initdb.d \
            -e POSTGRES_PASSWORD=password \
            -e POSTGRES_USER=user \
            -e POSTGRES_DB=postgres \
            -p 5433:5432 \
            --restart=always \
            -it postgres
        ;;
    # endregion

    # region app
    "run-admin")
        docker run \
            -p 8810:8810 \
            -e .env.docker \
            --restart=always \
            -it fast_drew_dru:latest \
            bash -c "./run.sh --docker"
        ;;
    # endregion
    # region celery
    # "run-redis")
    #     docker run \
    #         -v $(pwd)/redis.conf:/usr/local/etc/redis/redis.conf \
    #         -e .env.celery \
    #         -p 6379:6379 \
    #         --restart=always \
    #         --sysctl net.core.somaxconn=1024\
    #         -it redis:latest \
    #         bash -c "redis-server --appendonly yes --maxmemory 2048mb"
    #     ;;
    # "run-celery")
    #     docker run \
    #         -e .env.celery \
    #         --user python \
    #         --restart=always \
    #         -it pyimg2:latest \
    #         bash -c "celery worker -A coreMA.shared.workers:celery --loglevel=info -B"
    #     ;;
    # endregion
esac
