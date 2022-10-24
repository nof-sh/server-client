import logging
import selectors
import uuid
import socket
import DB
import protocol
from datetime import datetime

def stopServer(err):
    """ Print err and stop execution """
    print(f"\nFatal Error: {err}\n Server stoped!")
    exit(1)


def parsePort(file):
    """ read file for port number. Return port as integer. """
    port = 1234
    try:
        with open(file, "r") as portInfo:
            port = portInfo.readline().strip()
            port = int(port)
    except (ValueError, FileNotFoundError):
        port = 1234
    finally:
        return port
    

