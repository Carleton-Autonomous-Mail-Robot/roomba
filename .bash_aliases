alias BSH='source ~/.bashrc'
alias ps='ps aux'
alias T1='sudo usermod -a -G dialout $USER; cd create_ws; source devel_isolated/setup.bash; roslaunch ca_driver create_2.launch;'
alias T2='cd SAVI_ROS/rosjavaWorkspace/ ; source devel/setup.bash; cd /SAVI_ROS/rosjavaWorkspace/src/savi_ros_java/savi_ros_bdi/build/install/savi_ros_bdi/bin; ./savi_ros_bdi savi_ros_java.savi_ros_bdi.SAVI_Main;'
alias T3='cd create_ws; source devel_isolated/setup.bash; roslaunch saviRoomba roomba.launch;'
alias T4='cd create_ws; source devel_isolated/setup.bash; rosrun saviRoomba logger.py;'
alias T5='cd create_ws; source devel_isolated/setup.bash; rosrun saviRoomba userInterface.p;'

alias LAUNCH_T1='gnome-terminal -e "bash -c \"T1; exec bash\""'


