ssh pi@192.168.4.1 pkill screen
ssh pi@192.168.4.1 screen -ls
ssh pi@192.168.4.1 screen -S DAQ -d -m python3 "~/WT_Server/Offline_DAQ.py"
ssh pi@192.168.4.1 ps -u $USER
ssh pi@192.168.4.1 screen -ls