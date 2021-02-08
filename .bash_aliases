alias BSH='source ~/.bashrc'
alias ps='ps aux'
alias pull_project='cd ~/create_ws/src/Roomba; git pull; cd ~/'
alias T1='sudo usermod -a -G dialout $USER; cd ~/create_ws; source devel/setup.bash; roslaunch create_bringup create_2.launch;'
alias T2='cd ~/create_ws; source devel/setup.bash; roslaunch saviRoomba roomba.launch;'
alias T3='cd ~/create_ws; source devel/setup.bash; rosrun saviRoomba logger.py;'
alias T4='cd ~/create_ws; source devel/setup.bash; rosrun saviRoomba userInterface.p;'

alias LAUNCH_T1='gnome-terminal -e "bash -c \"T1; exec bash\""'


