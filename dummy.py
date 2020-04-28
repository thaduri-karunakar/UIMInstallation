import sys
import time
import dataPopulationGlobalVariable as gfile
from pypsexec.client import Client

def conenction():
    """ copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""
    try:
        global c
        c = Client(gfile.uimserver, gfile.username, gfile.password, encrypt='False')
        c.connect()
        c.create_service()
        # return c

    except Exception as e:
        print('Below exception occured .....\n')
        type, value, traceback = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        # print(e)
        print()

def connetion1():

    print('service created for following "{}".......\n\n'.format(gfile.uimserver))
    stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  hostname''')
    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')
    if rc == 0:
        print('net use command executed successfully : ', stdout)

def connetion2():

    print('service created for following "{}"=========================\n\n'.format(gfile.uimserver))
    stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  ipconfig''')
    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')
    if rc == 0:
        print('net use command executed successfully : ', stdout)


def remove():
        c.remove_service()
        c.disconnect()
        print("closed......")
conenction()
connetion1()

connetion2()
remove()
