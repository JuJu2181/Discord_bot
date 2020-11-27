import json
import pingparsing

def checkPing(destination_url):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = destination_url
    print(destination_url)
    transmitter.count = 10
    result = transmitter.ping()
    ping_details = ping_parser.parse(result).as_dict()
    #print(type(ping_details))
    print(ping_details)
    return ping_details


# data = checkPing("discord.com")
# print(data)
# print(type(data))
# print(data["packet_transmit"])

# import os

# def checkPing(destination_url):
#     hostname = destination_url
#     response = os.system("ping -c 1 " + hostname)
    
#     if response == 0:
#         print(hostname + " is up")
#     else:
#         print(hostname + " is down")

# checkPing('discord.com')

 
