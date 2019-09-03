#!/usr/bin/python3

# script to implement custom raspberry pi automated build...


import sys
import os
import os.path
from os import path
from subprocess import Popen as shell, PIPE
from shutil import copyfile
import json
import re

# declarations...
cfgFile="/boot/PiCafe/config.json"
taskFile="/boot/PiCafe/task"
cfgFile="PiCafe/config.json"
taskFile="PiCafe/task"
currentTask=int(open(taskFile,"r+").read().strip())

def resolveTask(task,vars):
  params = re.findall(r"%\w+",task['prompt'])
  task['log'] = task['prompt']
  for x in params:
    if x[1:] in vars: task['log'] = task['log'].replace(x,str(vars[x[1:]]))
    elif x[1:] in task: task['log'] = task['log'].replace(x,str(task[x[1:]]))
  params = re.findall(r"%\w+",task['cmd'])
  task['resolved'] = task['cmd']
  for x in params:
    if x[1:] in vars: task['resolved'] = task['resolved'].replace(x,str(vars[x[1:]]))
    elif x[1:] in task: task['resolved'] = task['resolved'].replace(x,str(task[x[1:]]))
  return task

# must be run as root...
if os.geteuid() != 0:
    exit("Script must be run as root.\nPlease try using 'sudo'...")

print("# Running bootstrap script with configuration '%s' starting with task %s" % (cfgFile,currentTask))

# read config file...
with open(cfgFile, 'r') as f:
  cfg = json.load(f)
  bootstrap = cfg["bootstrap"]  # shortcut
print ("# Configuration...\n",json.dumps(cfg,indent=2))

while currentTask <= len(bootstrap['tasks']):
  task = bootstrap['tasks'][currentTask-1]
  resolveTask(task,bootstrap)
  print('#',task['log'])
  print("CMD: %s" % task['resolved'])
  #shell(task['resolved'],shell=True).communicate()
  currentTask += 1
  open(taskFile,"w+").write(str(currentTask))
  if 'reboot' in task:
    print("# reboot before next task...")
    #shell('shutdown -r now',shell=True).communicate()
    exit()

# cleanup
# unmount the drives and remove the device and mountpoint before closing...
print("\n# cleanup ...")
print("# cleanup complete!")
print("# end")
