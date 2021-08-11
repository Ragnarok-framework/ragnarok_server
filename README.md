# Ragnarok Client
Ragnarok is an open source security framework for analysing vulnerability in network servers.

This repository contains the Ragnarok client, as well as an ephemeral form of the Diffie-Hellman key exchange. 
The client folder contains all the components nessecary for building the architecture

# Setup
This repo contains multiple inter-linked packages.
To import them locally, follow the instructions bellow
```
pip install cryptography  
```
After importing the modules, clone the repo
To start the client run:
```
python main.py
```
To define the different arguments you can use:
* ```-d``` or ```-debug``` - for outputting debug messages in the terminal
# Security Modules
The module folder in the source contains a port scanner and a tcp packet maker
# Port Scanner
To setup the port scanner you can do the folowing:
```python port_finder.py```
* ```--target_ip``` - defines the ip you want to scan
* ```-p``` - defines the port range
# TCP Packet Maker
To setup the port scanner you can do the following:
```python packet_maker.py```
* The target location can be changed using ```--dst```
* The predefined packet source can be changed using ```--src```
