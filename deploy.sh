#!/bin/bash
pkill -f app.py || true
python3 /home/ec2-user/todo-app/app.py &
