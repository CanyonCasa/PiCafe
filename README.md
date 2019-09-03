# PiCafe

#### Abstract

PiCafe implements a set of scripts that enable a fully automatic setup of a 
Raspberry Pi (RPi). A user simply defines all operations based on a JSON 
configuration file, **config.json**. After running a "patch" script, the 
RPi setup can proceed without any required user intervention. 

The process involves:

- Selecting a base image such as _2019-06-20-raspbian-buster-lite.img_
- Patching the image to enable PiCafe (Patch Script)
- Running the patched image in an RPi to complete setup.

## Preparing PiCafe

This section describes the build setup.

### File Tree

The examples here assume the following file tree layout:

 for a build folder 
that contains everything needed for creating an RPi install, including the 
Raspian source image file referenced by the build. 

- **Build folder**: Can have any name, holds everything needed for creating 
an RPi install, including the Raspian source image file referenced by the 
build. Execute scripts from the build folder.
  - **Raspian image files**: Source image required for the build
  - **PiCafe** Folder (from Github) holds all the other information 
  needed to create the install to organize and keep the setup clean.
    - **patch**: Folder containing the patch script and support files
    - **user**: See **_The user Folder_** section for details.
    - **config.json**: See **_Configuration File_** section for details.
    - **README.md**: This file
    - **bootstrap.sh**: Bash wrapper for calling user bootstrap user script.
    - **bootstrap.py**: Basic python file for defining the setup.
 
#### The user Folder

The user folder hold files and folders to be added to the image. The default 
bootstrap script maps the files and folders of this folder directly to the 
respective locations of the root partition. For example files in the folder 
_user/usr/local/bin_ would end up in _/usr/local/bin_. This enables the user 
to install personal utility scripts etc.

## Configuration File

**TBD**

## Patch Script

### Abstract

This section describes operations and elements of the **patch.py** script. 
The script prepares a Raspberry Pi image to enable automation of the PiCafe
installation utility. **patch.py** performs the following functions:

- Establishes a working image
- Executes a task list (which must include)
  - Loads the PiCafe folder
  - Patches the default init_resize.sh shell script
  - Patches the rc.local script to bootstrap setup

**IMPORTANT NOTE:**
**_All patch operations must be run on an image prior to running that image 
in an RPi._** Nominally, one RPi would be used to patch the image for 
another RPi using an USB SD adapter. Build completes when the patched card 
runs in another RPi.

#### Patch Script Execution

After defining a _config.json_ file, run the patch script as

    sudo PiCafe/patch/patch.py <PiCafe/config.json> 

See the **Patch Script** section below for details on its function and 
operation.

#### Patch Support Scripts and Files

**TBD**

### Establish Working Image (Device)...

The first step involves defining the working image. This represents the image
prepared by the patch script. The _source_ field under the _patch_ section of 
the _config.json_ file defines the (dd) image used to build the destination or 
working image, specified by the _dest_ field. If the _dest_ image matches the 
_source_ image or no _dest_ image is specified or the _source_ specifies a 
device (i.e. /dev/...), then the source becomes the working image. This 
behaviour supports two basic modes of operation:

- **Intermediate Builds**: Specifying different _source_ and _dest_ images 
allowsone to build an intermediate image from a pristine source, which can 
then be used to build other final images saving time replicating the patch 
process.
- **Direct Device Builds**: Specifying a /dev source means the image can be 
patched directly on a prepared SD card. In this case, an image can be pre-
loaded onto an SD card, patched, optionally saved as a _"golden image"_ and
then run in a RPi to complete the build.

#### Image Mounting and OS Requirements

PiCafe requires mounting the image file to make patches. Presently, this 
requires using Linux. The _mount_ field under the _patch_ section of 
the _config.json_ file defines the mountpoint. Reference this mountpoint 
in patch tasks, such as copying files. 

This script has been developed and tested specifically for Raspian 
distributions. **It will not work with NOOBS installations.**

### Execute Task List

The user may customize the task list to perform any number of setup tasks;
however, normally only task necessary to "patch" the Raspian build would be
performed at this stage. Tasks required for patching follow below.

#### Load PiCafe Setup Files

The PiCafe folder contains files needed for patch operations as well as any
scripts needed to support the build operations.

#### Fix init_resize.sh Script

On first boot, startup code runs the _/usr/lib/raspi-config/init_resize.sh_
script, which resizes the file system to fill available space on the SD card.
Unfortunately, this limits portability, causes problems when cloning images 
or restoring a setup when the replacement card has less useable space than 
the original. It also makes for larger image backups and prevents a user from
reserving space for other partitions, such as a data area.

To remedy this, patch includes a replacement _init_resize.sh_ script that 
looks for a _root_partition_resize_ file in the boot folder that allows the
user to specify the size for the root partition.

#### Fix /etc/rc.local on root partition

Raspian does not provide a hook to bootstrap a script to enable automating 
an OS installation.

To remedy this, patch includes a replacement _/etc/rc.local_ script that
calls _/boot/PiCafe/patch/rc.local_boot.sh_, if it exists. This enables 
a user to boot strap any script to automatically execute a series of 
operations to install any necessary software and configuration definitions
needed to fully define an RPi installation.

## Bootstrap Scripts

The _/etc/rc.local_ runs at every startup (for multi-user init states).
The patch process modifies the _/etc/rc.local_ file to call the 
_/boot/PiCafe/bootstrap.sh_ if it exists. By default this file invokes a
Python script, _/boot/PiCafe/bootstrap.py_, to complete the installation.
This script can make configuration changes, install software, run updates, 
and generally perform everything needed to complete the install.

Users can ...

1. Use the bootstrap scripts as defined with a custom configuration.
2. Replace the _/boot/PiCafe/bootstrap.py_ call in the shell script, 
_/boot/PiCafe/bootstrap.sh_, with a script of their chosing. Note: the 
image must contain the program needed to run the replacement script.
3. Extend the _/boot/PiCafe/bootstrap.sh_ to call an additional script.
NOTE: This needs to be done prior to patching the source image.
 



