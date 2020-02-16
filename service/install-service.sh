#!/usr/bin/env bash
# SYSTEMD SETUP

echo "Copying service file to /etc/systemd/system..."
systemd --version
# If you have 236+, uncomment the StandardOutput/Error lines in the service if you'd like to output
# logs and errors to custom locations. Else it's journalctl for you
sudo cp tavernbot.service /etc/systemd/system/

echo "Reloading daemon, enabling and starting tavernbot service"
sudo systemctl daemon-reload
systemctl status tavernbot # It should say 'not loaded'
sudo systemctl enable tavernbot
sudo systemctl start tavernbot
sleep 1
sudo journalctl -xe
# You should see healthy output and a logged-in message

echo "Setting up logrotate"
sudo ln -s $(pwd)/logrotate.tavern /etc/logrotate.d/
