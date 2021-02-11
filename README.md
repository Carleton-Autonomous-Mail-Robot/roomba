
# roomba

  

This is a prototype demo of a mail delivery system using an iRobot create (Roomba), with IR wall following and position detection using Bluetooth beacons. This prototype has is based on a project by Patrick Gavigan and Chidiebere Onyedinma, their orginal work can be found [here](https://github.com/NMAI-lab/saviRoomba)
  

This project connects an iRobot Create 2 (or 1) and utilizes the create_autonomy package, available at https://github.com/AutonomyLab/create_autonomy. 

The orginal progect utilized savi_ros_bdi, however, BDI and ros_java have been removed from this project to simplify.

## Overview

The project hopes to build off the orginal work, by increasing reliability of navigation, and providing a server client interface for robots to be sent on missions from a webapp. This will be achieved through the use of wall following and an indoor positioning system instead of line following and QR codes. The web-app can be found [here](https://github.com/Carleton-Autonomous-Mail-Robot/Web-App), and this robot will communicate with a [Python Flask REST service](https://github.com/Carleton-Autonomous-Mail-Robot/WebServices-Server).
  

## Configuration and Setup

A fresh installation of Rasbian Buster is recommended, however, Ubuntu 16.04 is prefered by [create_autonomy](https://github.com/AutonomyLab/create_robot) and may make installation far easier. We haven't persued this option yet, so try at your own initiative. It is recommended to use a Raspberry Pi 4, however, any computer should work!

### This installation is headless, the Raspberry Pi doesn't need a monitor, keyboard, or mouse
### 1. Installing Rasbian:
Please follow the latest rasbian install instructions found [here](https://www.raspberrypi.org/documentation/installation/installing-images/). Follow instructions for '*Using Raspberry Pi Imager*' for ease of use.

### 2. Set up Raspberry Pi:

 1. In the 'boot' partition of the SD card made in the guide above, create an empty file called '*ssh*'
 2. Plug Raspberry Pi into Ethernet, and power on
 3. Using Putty or a Terminal (if you have a Unix opperating system such as any Linux distro or Mac OS 10+), ssh into the raspberry pi using the address bellow.
> pi@raspberrypi.local

Note you may have the drop the .local from the end of the name.
Password: raspberry

4.  Run
> sudo raspi-config

5. Change the password and hostname of the raspberry pi to something else
6. Follow instructions to installing ROS from [here](http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi)
7. Follow the instructions for create_autonomy from [here](https://github.com/AutonomyLab/create_robot) (branch kinetic)
8. Clone this repo into your create workspace (create_ws/src)
9. Rebuild create workspace
10. Copy .bashrc and .bash_aliases from roomba repo and place them in your home directory

From now on, you can pull changes to the project just by running:
> pull_project 



  

## Running
Open a four terminals and run
> bash

In one terminal run (this is essential):
> T1
 
In the others run T2 to T4
