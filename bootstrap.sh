#!/bin/bash

# bootstrap script wrapper called from /etc/rc.local
# configure to run user script of choice...

echo "#################################################"
echo "Running ... $0"
echo "#################################################"

script="/boot/PiCafe/bootstrap.py"
task="/boot/PiCafe/task"

if [ -f "$task" ] && [ -f "$script" ]; then
  echo "Bootstrap script [ $bscript ] exists; executing at task $task ..."
  $script &
fi
