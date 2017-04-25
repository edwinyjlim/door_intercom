#!/bin/bash
#script to start a detached screen to run door intercom Flask app

clear

echo "Script begins..."

screen -d -m -S flaskapp bash -c "source ~/Desktop/door_intercom/venv/bin/activate; python ~/Desktop/door_intercom/app.py"

echo "Script finished."
