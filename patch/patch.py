#!/usr/bin/python3

# script to patch raspberry pi image for custom automated build...

import sys
import os
import os.path
from os import path
from subprocess import Popen as shell, PIPE
from shutil import copyfile
import json
import re

# declarations...
srcIsDevice = False

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

# process commandline...
if len(sys.argv)<2 or '-h' in sys.argv[1]:
  print("SYNTAX %s <config.json>" % sys.argv[0])
  exit(1)
if len(sys.argv)==3:
  [section,task] = (sys.argv[2]+':1').split(':')[0:2]
print("# Running build patch script...\n")

# define working files and folders...
scriptFolder = os.path.dirname(os.path.realpath(__file__))
wd = os.getcwd();
cfgFile = os.path.realpath(sys.argv[1])
print ('#',wd, scriptFolder, cfgFile)

# read config file...
with open(cfgFile, 'r') as f:
  cfg = json.load(f)
  patch = cfg["patch"]  # shortcut
print ("# Configuration...\n",json.dumps(cfg,indent=2))

# define working image...
if not path.exists(patch['source']):
  print ("# source image NOT found: %s" % patch['source'])
  exit(1)
if patch['source'].startswith('/dev'):
  srcIsDevice = True
  workingDev = patch['source']
elif not 'dest' in patch:
  workingImg = patch['source']
else:
  if not path.exists(patch['dest']):
    print("# copying %s to %s ..." % (patch['source'],patch['dest']))
    copyfile(patch['source'],patch['dest'])
  workingImg = patch['dest']

# connect image to device
if not srcIsDevice:
  print("# working image: ",workingImg)
  workingDev = shell('losetup --show -f -P "'+workingImg+'"',shell=True,stdout=PIPE).communicate()[0].rstrip().decode('ASCII')
print("# working device: ",workingDev)

# check or create mountpoint 
if not path.exists(patch['mount']):
  print("# creating mountpoint: ", patch['mount'])
  shell('mkdir '+patch['mount'],shell=True,stdout=PIPE).communicate()

# mount image device
rootMount = 'mount %sp2 %s' % (workingDev,patch['mount'])
print ("# root mount:",rootMount)
shell(rootMount,shell=True,stdout=PIPE).communicate()
bootMount = 'mount %sp1 %s/boot' % (workingDev,patch['mount'])
print ("# boot mount:",bootMount)
shell(bootMount,shell=True,stdout=PIPE).communicate()

# patch work...
print("\n# root listing...")
shell('ls '+patch['mount'],shell=True).communicate()
print("\n# boot listing...")
shell('ls '+patch['mount']+'/boot',shell=True).communicate()

for task in patch['tasks']:
  resolveTask(task,patch)
  print('#',task['log'])
  #shell(task['resolved'],shell=True).communicate()

print("\n# /etc/rc.local listing...")
shell('ls '+patch['mount']+'/etc/rc.local*',shell=True).communicate()
print("\n# boot listing...")
shell('ls '+patch['mount']+'/boot',shell=True).communicate()

# cleanup
# unmount the drives and remove the device and mountpoint before closing...
print("\n# cleanup ...")
print("# unmount %s/boot ..." % patch['mount'])
bootUMount = 'umount %s/boot' % patch['mount']
shell(bootUMount,shell=True,stdout=PIPE).communicate()
print("# unmount %s ..." % patch['mount'])
rootUMount = 'umount %s' % patch['mount']
shell(rootUMount,shell=True,stdout=PIPE).communicate()
print("# remove mountpoint %s ..." % patch['mount'])
shell('rmdir '+patch['mount'],shell=True,stdout=PIPE).communicate()
if not srcIsDevice:
  print("# remove device loop %s ..." % workingDev)
  shell('losetup -d "'+workingDev+'"',shell=True)
print("# cleanup complete!")
print("# end")
