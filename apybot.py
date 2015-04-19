#!/usr/bin/python3
#
# simple python IRC bot
#
# originally based on: http://archive.oreilly.com/pub/h/1968
# adapted to python 3, see also: https://gist.github.com/RobertSzkutak/1326452
# heavily modified
#
# cem, 2015-04-14
#

import asyncio
import time
import subprocess

class IRCBot(asyncio.Protocol):

    def __init__(self, loop, nick, channel):
        self.loop = loop
        self.nick = nick
        self.channel = channel

        self.readbuffer = ""

        self.user_set = False
        self.registered = False
        self.joined = False

### connection callbacks
    # (called once)
    def connection_made(self, transport):
        print("Connection made...")
        self.transport = transport

        self.identify_me()
        self.loop.create_task(self.join())
        self.loop.create_task(self.whatever())

    # (called once)
    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

### callbacks
    # (called when data is received)
    def data_received(self, data):
        print('Data received: {}'.format(data.decode()))
        self.parse_and_react(data)

    # further there is:
    # def eof_received()

### own methods

    def send_data(self, data):
        print("Sending: ", data)
        self.transport.write(data.encode("UTF-8"))

    def parse_and_react(self, data):
        self.readbuffer = self.readbuffer + data.decode("UTF-8")
        # (debug-print)
        #print("READBUFFER: ", self.readbuffer)

        temp = self.readbuffer.split("\n")
        self.readbuffer = temp.pop()

        for line in temp:
            line = line.rstrip()
            line = line.split()
            # (debug-print)
            #print("LINE: ", line)

            if (line[0] == "PING"):
                self.send_data("PONG {}\r\n".format(line[1]))

            elif (line[1] == "433"):
                # nick already in use
                self.nick = self.nick + "_"
                self.identify_me()

            elif (line[1] == "451"):
                # join but not registered
                # --> make retry check
                self.loop.create_task(join())

            elif (line[1] == "001"):
                # registered
                self.registered = True

            elif (line[1] == "353" and line[2] == self.nick and line[4] == self.channel):
                # joined channel
                self.joined = True

    def identify_me(self):
        self.send_data("NICK {}\r\n".format(self.nick))
        if (self.user_set == False):
            self.send_data("USER {} {} {} :Python bot!\r\n".format(self.nick, self.nick, self.nick))
            self.user_set = True

    @asyncio.coroutine
    def join(self):

        # give a slight timeout to let register
        yield from asyncio.sleep(3)
        self.send_data("JOIN {}\r\n".format(self.channel))

    def write_msg(self, msg):
        msg_list=msg.splitlines()
        for msg_item in msg_list:
            self.send_data("PRIVMSG {} :{}\r\n".format(self.channel, msg_item))

### "integrated" coroutines

    @asyncio.coroutine
    def whatever(self):
        while True:
            if not self.joined:
                print("Waiting...")
                yield from asyncio.sleep(1)
                continue

            print("Connected and joined...")

            # send a fortune
            fortune_msg = gen_fortune()

            self.write_msg(fortune_msg)

            yield from asyncio.sleep(20)

    @asyncio.coroutine
    def say_ho(self):
        while True:
            print("hii...")
            yield from asyncio.sleep(1)

# a separate coroutine
@asyncio.coroutine
def say_hi():
    while True:
        print("Hiii!")
        yield from asyncio.sleep(1)



FORTUNE_MAX_LENGTH="180"

def gen_fortune():
    '''Generate a fortune message.
Using fortune.'''
    # -s short
    fortune_cmd=['fortune', '-n'+FORTUNE_MAX_LENGTH, '-s']

    proc=subprocess.Popen(fortune_cmd, stdout=subprocess.PIPE)
    output=proc.communicate()[0]

    return output.decode('utf-8')
#    return output
#    out_dec=output.decode('utf-8')
#
    # wrap the text
#    out_wrap=textwrap.fill(out_dec, config.FORTUNE_WRAP_AT)
#
#    return out_wrap



def launch_bot_loop(server, nick, channel, port=6667):

    loop = asyncio.get_event_loop()

    conn = loop.create_connection(lambda: IRCBot(loop, nick, channel), server, port)

    loop.run_until_complete(conn)
    loop.run_forever()
    loop.close()


#launch_bot_loop("irc.freenode.netd", "pybot", "#test")
#launch_bot_loop("irc.freenode.net", "pybot", "#test")
launch_bot_loop("swisskomm.ch", "pybot", "#test")



