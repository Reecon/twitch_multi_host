'''
multi_host.py

Created on 28.07.2014

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

import bot, os, time, logging, argparse, configparser, inspect, json
from urllib import request


class MultiHost(object):
    '''
        
    '''
    def __init__(self, config):
        
        self.config = config
        
        self.server = config.get("twitch", "server")
        self.port = config.getint("twitch", "port")
        self.user = config.get("twitch", "user")
        self.auth = config.get("twitch", "auth")
        self.hostchannel = "#" + config.get("hosts", "hostchannel")
        
        
        self.ircbot = bot.IRCBot(self.server,
                                 self.port,
                                 self.user,
                                 self.auth,
                                 self.hostchannel)
        
        self.interval = self.config.getint("hosts", "default_interval")
        
        self.channels = self.config.get("hosts", "channels").split(",")
        
        self.lastcheck = time.time()
        self.checkinterval = 60
        
        self.lastswitch = time.time()
        
        
        self.onlinechannels = []
        self.showqueue = []
        
    def run(self):
        ''' connect to server '''
        self.ircbot.start()
        
        while 1:
            if time.time() - self.lastcheck > self.checkinterval: 
                ''' check online status '''
                print("check channels")
                self.onlinechannels.clear()
                for c in self.channels:
                    if self.is_channel_online(c):
                        self.onlinechannels.append(c)
                
                if not self.showqueue:
                    for o in self.onlinechannels:
                        self.showqueue.append(o)
                self.lastcheck = time.time()
                         
            if time.time() - self.lastswitch > self.interval:
                if self.showqueue:
                    print("host next")
                    nextchannel = self.showqueue.pop()
                    self.ircbot.host_chan(nextchannel)
                    self.lastswitch = time.time()
        
    
    def is_channel_online(self, channelname):
        """
        returns True if the channel is online, or False if it is offline
        """
        
        requesturl = "https://api.twitch.tv/kraken/streams/" + channelname
        jsonbytes = request.urlopen(requesturl).read()
        jsonstring = jsonbytes.decode("utf-8")
        
        streaminfo = json.decoder.JSONDecoder().decode(jsonstring)
        
        if streaminfo["stream"]:
            print((channelname + " is online").encode("UTF-8"))
            return True
        else:
            print((channelname +  " is offline").encode("UTF-8"))
            return False
        
        pass

if __name__ == '__main__':
    
    ''' setup logger '''
    
    
    ''' setup configparser '''
    config = configparser.ConfigParser()
    
    cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    conffile = cwd[:len(cwd)-3] + "twitch_multi_host.conf"
    print("conffile " + conffile)
    config.read(conffile)
    
    
    ''' setup argpser '''
    
    multihost = MultiHost(config)
    try:
        multihost.run()
    except KeyboardInterrupt:
        if multihost.ircbot:
            multihost.ircbot.shutdown()
    