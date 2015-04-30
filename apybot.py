#!/usr/bin/python3
#
# simple python IRC bot
#
# originally based on: http://archive.oreilly.com/pub/h/1968
# adapted to python 3, see also: https://gist.github.com/RobertSzkutak/1326452
# heavily modified
#
# Features:
# - asynchronous IO (using asyncio)
# - write quotes, on demand (using fortune)
# - periodic checking of hosts (using ping)
# - on demand checking of hosts (using ping)
#
# cem, 2015-04-14
#

import asyncio
import time
import subprocess


### Settings
# (test)
# IRC
IRC_SERVER = "swisskomm.ch"
IRC_BOTNICK = "apybot"
IRC_CHANNEL = "#test"

# Hosts/Servers to check
HOSTLIST = [ "localhost", "www.google.ch", "amd64box", "gugus" ]

# check interval in seconds
CHECK_TIMEOUT_S = 60

WARNMSG_1 = "WARNUNG: Kann host {} nicht erreichen..."
WARNMSG_2 = "(Ping returncode: {})"
# (real)
# --cut--

class IRCBot(asyncio.Protocol):

    def __init__(self, loop, nick, channel):
        self.loop = loop
        self.nick = nick
        self.channel = channel

        self.readbuffer = ""

        self.user_set = False
        self.registered = False
        self.joined = False

### connection callbacks (from asyncio.Protocol)
    # (called once)
    def connection_made(self, transport):
        print("Connection made...")
        self.transport = transport

        self.identify_me()
        # (call join when connected)
        #self.loop.create_task(self.join())

        self.loop.create_task(self.check_hosts_forever())

    # (called once)
    def connection_lost(self, exc):
        print("The server closed the connection.")
        print("Stop the event loop.")
        self.loop.stop()

### callbacks (from asyncio.Protocol)
    # (called when data is received)
    def data_received(self, data):
        print("Data received: {}".format(data.decode()))
        self.parse_and_react(data)

    # further there is:
    # def eof_received()

### own methods

## basic IRC handling

    def send_data(self, data):
        print("Sending: ", data)
        self.transport.write(data.encode())

    def parse_and_react(self, data):
        self.readbuffer = self.readbuffer + data.decode()
        # (debug-print)
        #print("READBUFFER: ", self.readbuffer)

        temp = self.readbuffer.split('\n')
        self.readbuffer = temp.pop()

        for line in temp:
            line = line.rstrip()

            # split the line
            # splitted line:
            # [0]: prefix
            # [1]: command
            # [2]: args
            # [3]: text
            sline = split_recv_msg(line)

            print(sline)

#            line = line.split()
            # (debug-print)
            #print("LINE: ", line)

            if (sline[1] == "PING"):
                self.send_data("PONG :{}\r\n".format(sline[3]))

            elif (sline[1] == "433"):
                # nick already in use
                self.nick = self.nick + "_"
                self.identify_me()

            elif (sline[1] == "451"):
                # join but not registered
                # --> make retry check
                print("Warning: JOIN {} failed. Retrying...".format(self.channel))
                self.join()

            elif (sline[1] == "001"):
                # registered
                self.registered = True
                self.join()

            elif (sline[1] == "353" and self.nick in sline[2] and self.channel in sline[2]):
                # joined channel
                self.joined = True

            elif (sline[1] == "PRIVMSG" and self.nick in sline[2]):
                # reply to a private message
                self.parse_private(sline[0], sline[3])


    def identify_me(self):
        self.send_data("NICK {}\r\n".format(self.nick))
        if (self.user_set == False):
            self.send_data("USER {} {} {} :Python bot!\r\n".format(self.nick, self.nick, self.nick))
            self.user_set = True

    def join(self):
        self.send_data("JOIN {}\r\n".format(self.channel))

    def write_msg(self, target, msg):
        msg_list = msg.splitlines()
        for msg_item in msg_list:
            self.send_data("PRIVMSG {} :{}\r\n".format(target, msg_item))

    def get_sender(self, prefix):
        '''Get the sender nick from a prefix.'''
        return prefix.split('!')[0]

## private conversation

    def parse_private(self, prefix, text):
        '''Parse a private message.'''

        # get the sender
        sender = self.get_sender(prefix)

        if (text == "quote"):
            self.reply_quote(sender)
        elif (text == "check"):
            self.checkhosts(sender)
        else:
            self.write_msg(sender, "I don't know...")

# replies/actions

    def reply_quote(self, sender):
        '''Reply with a fortune.'''

        fortune_msg = gen_fortune()

        self.write_msg(sender, fortune_msg)

    def checkhosts(self, sender):
        '''Check hosts on demand and reply.'''

        for hostname in HOSTLIST:
            ping_returncode = ping_host(hostname)

            self.send_check_result(sender, hostname, ping_returncode, False)

    def send_check_result(self, target, hostname, ping_ret, onlywarn=True):
        '''Send results.'''

        if ping_ret != 0:
            self.write_msg(target, WARNMSG_1.format(hostname))
            self.write_msg(target, WARNMSG_2.format(ping_ret))
        else:
            if not onlywarn:
                self.write_msg(target, "OK: Host {} erreicht.".format(hostname))
                self.write_msg(target, WARNMSG_2.format(ping_ret))

### "integrated" coroutines

    # (example)
#    @asyncio.coroutine
#    def whatever(self):
#        while True:
#            if not self.joined:
#                print("Waiting...")
#                yield from asyncio.sleep(1)
#                continue
#
#            print("Connected and joined...")
#
#            # send a fortune
#            #fortune_msg = gen_fortune()
#
#            #self.write_msg(fortune_msg)
#
#            yield from asyncio.sleep(1)

    # (example)
#    @asyncio.coroutine
#    def say_ho(self):
#        while True:
#            print("hii...")
#            yield from asyncio.sleep(1)

    @asyncio.coroutine
    def check_hosts_forever(self):
        '''Check periodically if hosts are up.'''

        # (wait until joined)
        while True:
            if not self.joined:
                print("Waiting...")
                yield from asyncio.sleep(1)
                continue

            # checking hosts
            for hostname in HOSTLIST:
                ping_returncode = ping_host(hostname)

                # notify (only if not reachable)
                self.send_check_result(IRC_CHANNEL, hostname, ping_returncode)

            # timeout
            yield from asyncio.sleep(CHECK_TIMEOUT_S)

### separate coroutines

# (example)
#@asyncio.coroutine
#def say_hi():
#    while True:
#        print("Hiii!")
#        yield from asyncio.sleep(1)

### functions

def split_recv_msg(line):
    '''Split received IRC message into defined parts.

Returns: prefix command args text'''

    prefix = None
    text = None

    if line[0] == ':':
        prefix, line = line[1:].split(' ', 1)

    if line.find(' :') != -1:
        line, text = line.split(' :', 1)

    if line.find(' ') != -1:
        command, line = line.split(' ', 1)
        args = line.split()
    else:
        command = line
        args = None

    return prefix, command, args, text


FORTUNE_MAX_LENGTH="180"

def gen_fortune():
    '''Generate a fortune message.
Using fortune.'''
    # -s short
    fortune_cmd=['fortune', '-n'+FORTUNE_MAX_LENGTH, '-s']

    proc=subprocess.Popen(fortune_cmd, stdout=subprocess.PIPE)
    output=proc.communicate()[0]

    return output.decode()


def ping_host(hostname):
    # ping host and return the returncode

    ping_cmd = [ "ping", "-c1", "-w60", hostname ]

    proc = subprocess.Popen(ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #proc = subprocess.Popen(ping_cmd)

    # (set out, err needed ?)
    proc.communicate()

    return proc.returncode


def launch_bot_loop(server, nick, channel, port=6667):

    loop = asyncio.get_event_loop()

    conn = loop.create_connection(lambda: IRCBot(loop, nick, channel), server, port)
    loop.run_until_complete(conn)
    loop.run_forever()
    loop.close()


launch_bot_loop(IRC_SERVER, IRC_BOTNICK, IRC_CHANNEL)
