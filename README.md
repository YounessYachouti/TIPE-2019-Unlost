# Unlost
Unlost - An open source luggage manager for airports <br/>
__This project was made for the TIPE 2019 test__

This program can be used in airports to manage luggages, and prevent sending luggages to the wrong airplane and losing them.

## Concept
Luggage infos are hosted in a database within a server
Each luggage is associated with a unique RFID tag

This program has 3 modes :
- Registering new luggages
- Checking if a luggage belongs to a flight
- Resetting a tag to be reused

### Registering new luggages
In this mode the program waits for a tag in a serial port;
When the airport employee scans a card with the RFID reader system,
if the card is not already in use, the program will demand the informations related to the flight
then when everything is ok, an entry will be inserted in the database.

### Checking if a luggage belongs to a flight
First of all, the program prompts for the flight name,then waits for a tag in a serial port;
When a card is detected, the program will check if the luggage associated with this card belongs to the flight
if it does, it will be ignored, if it doesn't it will be reported.

### Resetting a tag to be reused
When a card is detected, it will be reset for future reuse

# How to install
After configuring your server and database,
and after installing python 3.7 (it may work in 3.6 but it is not tested there)

do the following :
1. install mysql.connector module from the official mysql [site](https://downloads.mysql.com/archives/c-python/)
2. install pyserial using pip (you can install it manually if you want)
```
python -m pip install pyserial
```
or
```
$ pip install pyserial
```
3- run the program using the command line, with its required arguments
```
$ main.py --help

usage: main.py [-h] H DB U [P]

   Luggage management program

   positional arguments:
    H           the server ip
    DB          the database name
    U           username
    P           password

   optional arguments:
         -h, --help  show this help message and exit

```

# How to use
Just follow the instructions that the program gives you


