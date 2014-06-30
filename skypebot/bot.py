__author__ = 'superpeanut911'
import Skype4Py
import time
import urllib
import json
import shlex
import os

#Get a skype instance
skype = Skype4Py.Skype()
#Attach to whatever skype is currently open
skype.Attach()


#Message Listener
def OnMessageStatus(Message, Status):
    body = Message.Body
    #Make sure every message starts with ! before doing anything
    if Status == 'RECEIVED' or Status == 'SENT' and body.startswith("!"):

        if body == "!info" or body == "!help":
            #Please don't take my name out of this <3
            Message.Chat.SendMessage("mc.ecb-mc.net Skype Bot by superpeanut911! Use '!exit' to stop the bot, "
                                     "'!uuid <player>' to get the player's UUID, "
                                     "and '!mcping <ip>:[port]' to ping a server!")

        if body == "!exit":
            Message.Chat.SendMessage("Shutting down bot... bai!")
            os._exit(0)

        if body.startswith("!uuid"):
            uuidmsg = shlex.split(body)
            try:
                data = getPlayerUUID(uuidmsg[1])
                Message.Chat.SendMessage("UUID for player " + data[0]["name"] + " is: " + data[0]["uuid"])
            except:
                Message.Chat.SendMessage("Error! Usage: '!uuid <playername>'")

        if body.startswith("!mcping"):
            msg = shlex.split(body)
            try:
                data = getPingData(msg[1])

                if data["status"] == "false":
                    Message.Chat.SendMessage("Error: " + data["error"])
                    print "Error! Is the server online? Is the IP correct?"
                elif data["status"] == "true":
                    Message.Chat.SendMessage("Players Online: " + data["players"]["online"] +
                                             "/" + data["players"]["max"] +
                                             "! Ping time: " + data["ping"] + "ms")
            except:
                Message.Chat.SendMessage("Error! Usage: '!mcping <ip>:[port]'")


def getPingData(ip):
    url = "http://mcapi.ca/v2/query/info/?ip=" + ip
    r = urllib.urlopen(url)
    data = json.loads(r.read())
    return data


def getPlayerUUID(player):
    url = "http://mcapi.ca/uuid/?player=" + player
    r = urllib.urlopen(url)
    data = json.loads(r.read())
    return data

#Connect the function and event
skype.OnMessageStatus = OnMessageStatus
print "Bot by superpeanut911 ready! Use '!info' to test me!"

while 1:
    time.sleep(1)
