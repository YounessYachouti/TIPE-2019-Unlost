#
# Main program for the Luggage management system
# Coded by Y.Youness (Yunusu) for the TIPE 2019 project
#

import argparse, serial, os, sys, signal
from api.unlost_api import *

signal.signal(signal.SIGINT, lambda x,y: end())

# clears the screen
def clearScreen():
   if os.name =='posix': # Linux machines
       os.system('clear')
   else:                 # windows machines ?
       os.system('cls')
# Just a simple menu system
def ask(question, choices, message=""):
    msg = message
    choice = None
    while(choice == None):
        clearScreen()
        print(question + " ( type 0 to exit )")
        if(len(msg)>0):
            print("\n Alert : " +msg)
        for n in range(len(choices)):
            print("\t "+str(n+1)+"| "+ choices[n])
        try:
            choice = int(input(" >"))
        except ValueError:
            msg = "Invalid choice ! Type a number between 1 and "+str(len(choices))+" or type 0 to exit"
            continue
        if not (choice in range(0,len(choices)+1)):
            choice = None
            msg = "Invalid choice !"
            continue
    if(choice == 0):
        end()
    return (choice, choices[choice-1])

def prompt(field):
    result = ""
    while len(result)==0:
        result = input(field+" : ")
    return result

def normalize(checksum):
    for i in range(len(checksum)):
        checksum[i] = str(checksum[i]).replace("b'","")
        checksum[i] = str(checksum[i]).replace("'","")
        checksum[i] = int(checksum[i])
    return checksum
def end():
    if 'client' in vars() or 'client' in globals():
        print("\n\n Disconnecting...")
        client.unlost_disconnect()
    if 'ser' in vars() or 'ser' in globals():
        print("\n Closing the port...")
        ser.close()
    print("\n Exit..")
    exit()

# *********************
#     Main functions
# *********************

# Reads a tag then add a flight associated with it after checking that the card isn't already in use
def terminal_register():
    while(True):
        clearScreen()
        print("\t    ******  Registering new luggages  ******")
        print("\t       **********************************   ")
        print("\nScan a card with the RFID card reader system ")
        print("Then you will be prompted for the flight informations")
        print("\n\n")
        print("\t\tWaiting for a card ...")
        # read 40 bytes from the serial port
        tag = ser.read(40)
        # split the result with ' '  (eg.   b'12 34 56'   becomes   [b'12',b'34',b'56'])
        tag = tag.split(b' ')
        # trim the tag, to keep just the checksum
        checksum = tag[5:len(tag)-2]

        # if the tag isn't empty
        if tag != [b'']:
            chacksum = normalize(checksum)

            clearScreen()
            print("\t    ******  A card has been detected  ******")
            print("\t       **********************************   ")
            print(" tag checksum : "+ str(checksum))
            print("\n Checking if the card is already in use ...\n")
            client.unlost_refresh()
            flights = client.unlost_get_flight("tag = '"+str(checksum)+"'")
            is_a_valid_card = True
            current_flight = None
            if(len(flights) > 0):
                for i in range(len(flights)):
                    if flights[i][len(flights[i])-1] == 0:
                        is_a_valid_card = False
                        current_flight = i
                        break
            if not is_a_valid_card:
                print("This card is already in use !\n")
                print("flight details : ")
                print(flights[current_flight]) # TODO print details in a readable way
                print("\n - press ENTER to continue - ")
                input()
                continue

            print("This card is valid !")
            print("\n Enter the informations to register : (type _SKIP_ in a field to skip this card)")

            first_name = prompt("first name")
            if(first_name == "_SKIP_"): continue
            last_name = prompt("last name")
            if(last_name == "_SKIP_"): continue
            passport = prompt("passport")
            if(passport == "_SKIP_"): continue
            departure = prompt("departure")
            if(departure == "_SKIP_"): continue
            destination = prompt("destination")
            if(destination == "_SKIP_"): continue
            flight = prompt("flight")
            if(flight == "_SKIP_"): continue

            print(" Please verify that informations are correct ")
            if(prompt(" Register this fight ? (Y/N)")!="Y"):
                continue
            client.unlost_add_flight(str(checksum), passport, first_name, last_name, departure, destination, flight)


def terminal_check():
    flight_name = prompt("Flight name ")

    while(True):
        clearScreen()
        print("\t    ******  Checking luggages  ******")
        print("\t       ***************************   ")
        print("\n")

        print("\nScan a card with the RFID card reader system ")
        print("\n\n")
        print("\t\tWaiting for a card ...")
        # read 40 bytes from the serial port
        tag = ser.read(40)
        # split the result with ' '  (eg.   b'12 34 56'   becomes   [b'12',b'34',b'56'])
        tag = tag.split(b' ')
        # trim the tag, to keep just the checksum
        checksum = tag[5:len(tag)-2]

        # if the tag isn't empty
        if tag != [b'']:
            chacksum = normalize(checksum)

            clearScreen()
            print("\t    ******  A card has been detected  ******")
            print("\t       **********************************   ")
            print(" tag checksum : "+ str(checksum))
            print("\n Checking if the luggage belongs to this flight ... \n")
            client.unlost_refresh()
            flight = client.unlost_get_flight("tag = '"+str(checksum)+"' AND status = 0")
            if(len(flight) == 0):
                print("This card don't correspond to any flight")
                print("\n - press ENTER to continue - ")
                input()
            else:
                if(flight[0][7] != flight_name):
                    print("\aWARNING !")
                    print("This luggage doesn't belong to this flight !")
                    print("\n")
                    print("\n - press ENTER when you are ready to continue - ")
                    input()

def terminal_reset():
        while(True):
            clearScreen()
            print("\t    ******  Resetting a Tag  ******")
            print("\t       *************************   ")
            print("\nScan a card with the RFID card reader system ")
            print("\n\n")
            print("\t\tWaiting for a card ...")
            # read 40 bytes from the serial port
            tag = ser.read(40)
            # split the result with ' '  (eg.   b'12 34 56'   becomes   [b'12',b'34',b'56'])
            tag = tag.split(b' ')
            # trim the tag, to keep just the checksum
            checksum = tag[5:len(tag)-2]

            # if the tag isn't empty
            if tag != [b'']:
                chacksum = normalize(checksum)

                clearScreen()
                print("\t    ******  A card has been detected  ******")
                print("\t       **********************************   ")
                print(" tag checksum : "+ str(checksum))
                print("\n Checking if the card is in use ...\n")
                client.unlost_refresh()
                flights = client.unlost_get_flight("tag = '"+str(checksum)+"'")
                is_in_use = False
                current_flight = None
                if(len(flights) > 0):
                    for i in range(len(flights)):
                        if flights[i][len(flights[i])-1] == 0:
                            is_in_use = True
                            current_flight = i
                            break
                if not is_in_use:
                    print("This card is already reset, and can be reused\n")
                    print("\n - press ENTER to continue - ")
                    input()
                    continue

                print("\nThis card is in use")
                print("flight details : ")
                print(flights[current_flight]) # TODO print details in a readable way

                if(prompt(" Reset this card ? (Y/N)")!="Y"):
                    continue
                client.unlost_flight_set_status("id = "+str(flights[current_flight][0]), 1)


#               Setting up arguments
#**************************************************
#
#   usage: main.py [-h] H DB U [P]
#
#   Luggage management program
#
#   positional arguments:
#    H           the server ip
#    DB          the database name
#    U           username
#    P           password
#
#   optional arguments:
#         -h, --help  show this help message and exit
#

parser = argparse.ArgumentParser(description='Luggage management program')
parser.add_argument('host', metavar='host', type=str, nargs=1,
                   help='the server ip')
parser.add_argument('database', metavar='database', type=str, nargs=1,
                   help='the database name')
parser.add_argument('username', metavar='username', type=str, nargs=1,
                   help='username')
parser.add_argument('password', metavar='password', type=str, nargs='?',
                   help='password', default='')

args = parser.parse_args()

flights_table = prompt("flights table name ")

print("Connecting to "+str(args.host[0])+" . . .")


#   Tries to connect to the database with the given arguments
try:
    client = Unlost(args.host[0], args.username[0], args.password, args.database[0],flights_table)
except:
    print("Connection error")
    exit()
try:
    client.unlost_get_flight("id = 1")
except:
    print("Table not found ! exit..")
    exit()

print("Connected successfully ")

is_serial_ready = False
msg = ""
while not is_serial_ready:
    port = ask("Which port should the program use to recieve RFID data ? ", ['COM1','COM2','COM3','COM4'],msg)[1]
    try:
        # initialize the serial port to recieve data from arduino
        ser = serial.Serial(port,9600,timeout=1)
        # close serial port then open it (to be sure it is closed first)
        ser.close()
        ser.open()
    except serial.serialutil.SerialException:
        msg = "Could not open the specified port, you specified the wrong port or the RFID tag reader system is not connected or the port is already used by another program "
        continue
    is_serial_ready =True


print("Serial port is ready ")

# Main menu
clearScreen()

choice = int(ask(
    """\t    ******  Welcome to the luggage management program  ******
    \t    ******    This program was made by a rain lover    ******
    \t               **********************************
    \n Connected to """+args.host[0]+""" \t | \t """+"Recieving RFID data on port : """+port+"""
    \nWhat does this terminal do ?""",
    ['Register new luggages','Checks if a luggage belongs to a certain flight','Resets a flight'],msg)[0])

try:
    # Perform the chosen action
    if(choice == 0):
        exit()
    if(choice == 1):
        terminal_register()
    elif(choice == 2):
        terminal_check()
    elif(choice == 3):
        terminal_reset()
except:
    end()
