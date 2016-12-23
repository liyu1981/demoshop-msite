#!/bin/bash
python manage.py runsslserver 0.0.0.0:5566 --certificate /etc/letsencrypt/live/didi-ads.com/cert.pem --key /etc/letsencrypt/live/didi-ads.com/privkey.pem &
