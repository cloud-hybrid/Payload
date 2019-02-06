@echo off
timeout /t 15 /nobreak
start cmd /k "ssh snow@192.168.1.5 -t virsh console Windows-Test"
