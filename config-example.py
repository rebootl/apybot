# Settings for apybot

# IRC
IRC_SERVER = "irc.example.org"
IRC_BOTNICK = "apybot"
IRC_CHANNEL = "#test"

# Hosts/Servers to check
HOSTLIST = [ "localhost", "www.google.ch", "amd64box", "gugus" ]

# check interval in seconds
CHECK_TIMEOUT_S = 60

WARNMSG_1 = "WARNUNG: Kann host {} nicht erreichen..."
WARNMSG_2 = "(Ping returncode: {})"

# anti-flood delay in seconds
ANTI_FLOOD_DELAY = 1

# fortune quotes
FORTUNE_MAX_LENGTH="180"
FORTUNE_PATH="/usr/games/fortune"

# error msgs
IDK_ERR = "I don't know..."
FUNCOMM_ERR = "funcom must start with a ! and otherwise only contain letters and numbers..:p"
