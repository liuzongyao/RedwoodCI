#!/bin/bash
set -e
if [ ! -f "/RedwoodHQ/public/automationscripts/Sample/admin/bin/flag.sh" ];then
    echo "no data found, need to copy"
    cp -R /automationscripts /RedwoodHQ/public
else
    echo "data found, do nothing"
fi
rm -rf /RedwoodHQ/public/automationscripts/Sample/admin/PythonWorkDir
virtualenv --no-pip --no-setuptools --no-wheel /RedwoodHQ/public/automationscripts/Sample/admin/PythonWorkDir
node app.js &
echo "RedwoodHQ started"
node agent/app.js 
echo "RedwoodHQ Agent started"
