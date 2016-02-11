#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
      


#=============================
# Common Class for Doom definitions
#=============================
class DoomCommon():

    bFillWithConfig = True;
    WWWURL = "";
    Mail = "";
    IWAD = "";
    PWAD = "";   
    Host_Prefix = "";
    Hostname = "";
    Password = "";
    JoinPassword = "";
    
    def __init__ (self, filename):
        self.autocfg = configparser.ConfigParser();
        self.autocfg.read(filename);
    
    def ReplaceOS(self, platform, text):
        if (platform == 0):
            return text.replace("#","::");
        return text;
    
    def ClampQuestion (self, min, max, message, question):
        number = -1;
        while ( int(number) < min or int (number) > max):
            try:
                if (message is not ""):
                    print (message);
                number = int(input(question+" ["+str(min)+"-"+str(max)+"]: "));
            except ValueError:  
                continue;
            
        return number;

    ###
    # ASK_Password
    # Asks to input your mail address (sv_contact). -- Automatically gives the one used
    ###    
    def ASK_Password(self):
        self.Password = str(input("If you want to input a server password, type it in. Else, leave it empty: "));
        self.JoinPassword = str(input("If you want to input a server join password, type it in. Else, leave it empty: "));
        
    ###
    # ASK_MailAddress 
    # Asks to input your mail address (sv_contact). -- Automatically gives the one used
    ###    
    def ASK_MailAddress(self):
        self.Mail = self.autocfg['Common']['Mail'];
        if (self.Mail):
            print(">>> [INFO] Using Saved Mail address.")
            return;
        self.Mail = str(input("Please input your mail address: "));
      
    ###
    # ASK_WebAddress 
    # Asks to input the Web address.
    ###        
    def ASK_Hostname(self):
        self.Host_Prefix = self.autocfg['Common']['Hostname_Prefix'];
        
        if (self.Host_Prefix):
            print(">>> [INFO] Using Saved Server Prefix.");
        prename = input('Please input your hostname: '+self.Host_Prefix+' ');
        self.Hostname = (self.Host_Prefix + " " + prename);
            
    ###
    # ASK_WebAddress 
    # Asks to input the Web address.
    ###        
    def ASK_WebAddress(self):
        self.WWWURL = self.autocfg['Common']['Web'];
        if (self.WWWURL):
            print(">>> [INFO] Using Saved Web address.")
            return;
        self.WWWURL = str(input("Please input a Web Address for remote-downloading PWADs: "));

    def IWAD_Name(self, IWAD):
        if (IWAD == 1): return "DOOM.WAD"; # The Ultimate DOOM
        elif (IWAD == 2): return "DOOM2.WAD"; # DOOM 2
        elif (IWAD == 3): return "TNT.WAD"; # TNT
        elif (IWAD == 4): return "PLUTONIA.WAD"; # The Plutonia Experiment
        return "DOOM2.WAD"; #Default IWAD
    
    ###
    # ASK_IWAD 
    # Asks for the IWAD through the name
    ###
    def ASK_IWAD(self):  
        msg = "What IWAD would you like to use?\n\
[1] The Ultimate DooM\n\
[2] Doom 2\n\
[3] TNT\n\
[4] The Plutonia Experiment";  
        iChoice = self.ClampQuestion(1, 4, msg, "> Select");
        self.IWAD = (self.IWAD_Name(iChoice))
        
    ###
    # ASK_PWAD 
    # Asks to input the PWADs, if any.
    ###        
    def ASK_PWAD(self):
        self.PWAD = str(input("If you want to use PWADs, type them in. Else, leave it empty: "));