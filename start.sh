#!/bin/sh

docker build -t ods-emailrestinterface .; \
docker run \
   -p 10010:10010 \
   -e EMAIL_USE_TLS=False \
   -e EMAIL_LOGIN=False \
   -e MESSAGE_WORKER_EMAIL_GATEWAY_URI=172.17.0.1:1025 \
   ods-emailrestinterface

