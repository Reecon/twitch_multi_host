'''
bot.py

Created on 30.07.2014

@author: reecon

Copyright (c) 2014

GNU GENERAL PUBLIC LICENSE

    This file is part of twitch_multi_host.

    twitch_multi_host is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    twitch_multi_host is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with twitch_multi_host.  If not, see <http://www.gnu.org/licenses/>.

 
'''

import socket, sys

class IRCBot(object):
    '''
    classdocs
    '''


    def __init__(self, server, port, user, password, hostchannel):
        '''
        Constructor
        '''
        self.server = server
        self.port = port
        self.user = user
        self.pw = password
        self.hostchannel = hostchannel
        
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect_to_server_(self):
        print("connect")
        self.ircsock.connect((self.server, self.port))
        print("user")
        print(self.ircsock.send(("USER " + self.user + " " + self.user + " " + self.user + " : care_o_bot\n").encode("UTF-8")))
        print("pass")
        print(self.ircsock.send(("PASS " + self.pw + "\n").encode("UTF-8")))
        print("nick")
        print(self.ircsock.send(("NICK " + self.user + "\n").encode("UTF-8")))
        self.join_channel_(self.hostchannel)
        print("connectet to " + self.hostchannel)
    
    def join_channel_(self,chan):
        print("join")
        print(self.ircsock.send(("JOIN "+ chan + "\n").encode("UTF-8")))
    
    def ping(self):
        print("pong")
        print(self.ircsock.send(("PONG :Pong\n").encode("UTF-8")))
        
    def sendmsg(self, chan, msg):
        print("send")
        print(self.ircsock.send(("PRIVMSG " + chan + " :" + msg + "\n").encode("UTF-8")))
        
    def host_chan(self, chan):
        print("host")
        print(self.ircsock.send(("PRIVMSG " + self.hostchannel + " :/host " + chan + "\n").encode("UTF-8")))
        
    def unhost(self):
        print("unhost")
        print(self.ircsock.send(("PRIVMSG " + self.hostchannel + " :/unhost\n").encode("UTF-8")))    
        
    def shutdown(self):
        self.unhost()
        print("part")
        print(self.ircsock.send(("PART "+ self.hostchannel + "\n").encode("UTF-8")))
        print("quit")
        print(self.ircsock.send(("QUIT off for now").encode("UTF-8")))
        print("close socket")
        self.ircsock.close()
    
    def start(self):
        print("startbot")
        self.connect_to_server_()
        #self.run()
    
    def run(self):
        while 1:
            ircmsg = self.ircsock.recv(2048)
            ircmsg = ircmsg.decode("UTF-8")
            ircmsg = ircmsg.strip('\r\n')
            print(ircmsg)
            
            if ircmsg.find("PING :") != -1:
                self.ping()
            
            #only host can trigger commands
            if ircmsg.find(":" + self.hostchannel + "!") != -1:
                
                if ircmsg.find(":!hello") != -1:
                    self.sendmsg(self.hostchannel, "Hello")
                    
                if ircmsg.find(":!shutdown") != -1:
                    self.shutdown()
                    sys.exit()
                    
    