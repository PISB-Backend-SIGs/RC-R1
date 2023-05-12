#!/bin/bash
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d
sudo systemctl reload nginx
