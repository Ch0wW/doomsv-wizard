#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys;
import getopt;
import platform;

# Doom Classes
import doomsv.common as common
import doomsv.zdaemon as ZDaemonServer
#import doomsv.zandronum as ZandronumServer
#import doomsv.odamex as OdamexServer
import doomsv.prboom as PrBoomServer
import doomsv.chocodoom as ChocoServer 

def main (args):
	
    # Common Elements
    doom = common.DoomCommon("doomconfig.ini");

    #Check Arguments
    #-- Destination System
    #if (False):
    #    print ("Unsupported Argv yet");
    #else:
    strOS = platform.system();
	
	#Select Port
    msg_choice = "What port of Doom would you like to make a server?\n\
[1] Chocolate Doom / Dos Doom\n\
[2] PrBoom+\n\
[3] Zdaemon (Unsupported yet)"; 

    """
    \n\
    [4] Zandronum\n\
    [5] Odamex
    """

    iSelectedPort = doom.ClampQuestion(1,3, msg_choice, "Your choice");

    if (iSelectedPort == 1):
        port = ChocoServer.ChocoDoomServer(doom, strOS);
    elif (iSelectedPort == 2):
        port = PrBoomServer.PrBoomServer(doom, strOS);
    elif (iSelectedPort == 3): 
        port = ZDaemonServer.ZDaemonServer(doom);
    elif (iSelectedPort == 4):
        return;
#       port = ZandronumServer.ZandronumServer(doom);	
    elif (iSelectedPort == 5):
        return;
#       port = OdamexServer.OdamexServer(doom);	
    else:
        print ("Unknown Port, or unsupported choice/parameter.");
        return;
		
    port.Run();
	
if __name__ == "__main__":
    main(sys.argv[1:])