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
    
class Server:
    DB = 'server.db'
    PACKET_SIZE = 1024   # Default packet size.
    MAX_QUEUED_CONN = 5  # Default maximum number of queued connections.
    IS_BLOCKING = False  # Do not block!

    def __init__(self, host, port):
        """ Initialize server. Map request codes to handles. """
        logging.basicConfig(format='[%(level)s -- %(time)s] -- %(note)s', level=logging.INFO, datefmt='%H:%M:%S')
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.db = DB.Database(Server.DB)
        self.err = ""  # error description.
        self.requests = {
            protocol.ERequestCode.REQUEST_REGISTRATION.value: self.handleRegistrationRequest,
            protocol.ERequestCode.REQUEST_USERS.value: self.handleUsersListRequest,
            protocol.ERequestCode.REQUEST_PUBLIC_KEY.value: self.handlePublicKeyRequest,
            protocol.ERequestCode.REQUEST_SEND_MSG.value: self.handleMessageSendRequest,
            protocol.ERequestCode.REQUEST_PENDING_MSG.value: self.handlePendingMessagesRequest
        }