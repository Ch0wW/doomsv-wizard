#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import date;
import json;    

GAMEMODE_DM = 1;
GAMEMODE_TDM = 2;
GAMEMODE_COOP = 3;
GAMEMODE_CTF = 4;
GAMEMODE_SURV = 5;
GAMEMODE_DDOM = 6;
GAMEMODE_KOTH = 7;

SORT_DUEL = 0
SORT_FFA = 1
SORT_COOP = 2
SORT_TDM = 3
SORT_CTF = 4
SORT_DDOM = 5
SORT_KOTH = 6

#=============================
# Zdaemon Class for generating a server.
#=============================
class ZDaemonServer():

    common = "";
    dmflags = 0;
    dmflags2 = 0;
    maxlives = 1;
    bDuelEnabled = False;
    tDmflags = "";
    tDmFlagsGamemode = [[] for _ in range (0,7)];
    
    
    def __init__(self, commonclass):
        self.common = commonclass;
        
        # Sort the Zdaemon json file through a local array.
        with open ("dmflags/zdaemon.json") as filename:
            tDmflags = json.load(filename);
            
        for element in tDmflags:            
            # Register allowed values.
            if (element['gamemode'] == 0 and element['duel'] == 1):
                self.tDmFlagsGamemode[SORT_DUEL].append(element);
            elif (element['gamemode'] == 0 and element['duel'] == 0):
                self.tDmFlagsGamemode[SORT_FFA].append(element);
            elif (element['gamemode'] == 1):
                self.tDmFlagsGamemode[SORT_TDM].append(element);
            elif ( (element['gamemode'] == 2 or element['gamemode'] == 4) and element['cooperative'] == 1):
                self.tDmFlagsGamemode[SORT_COOP].append(element);
            elif (element['gamemode'] == 3):
                self.tDmFlagsGamemode[SORT_CTF].append(element);
            elif (element['gamemode'] == 5):
                self.tDmFlagsGamemode[SORT_DDOM].append(element);
            elif (element['gamemode'] == 6):
                self.tDmFlagsGamemode[SORT_KOTH].append(element);
                
        # ToDo: Count total configurations
        print ("Total of templates: "+str(len(self.tDmFlagsGamemode[0])+len(self.tDmFlagsGamemode[1])+len(self.tDmFlagsGamemode[2])+len(self.tDmFlagsGamemode[3])+len(self.tDmFlagsGamemode[4])+len(self.tDmFlagsGamemode[5])+len(self.tDmFlagsGamemode[6])))
#        print (self.tDmFlagsGamemode[0])
        
    ###
    # ASK_Gamemode 
    # Asks to input the gamemode chosen.
    ###   
    def Gamemode_Name(self, mode):
        if   (mode == GAMEMODE_DM):   return "Deathmatch"; 
        elif (mode == GAMEMODE_TDM):  return "Team Deathmatch";
        elif (mode == GAMEMODE_COOP): return "Cooperation";
        elif (mode == GAMEMODE_CTF):  return "Capture the Flag";
        elif (mode == GAMEMODE_SURV): return "Survival";
        elif (mode == GAMEMODE_DDOM): return "Double Domination";
        return "Deathmatch"; #Default Mode
        
    def ASK_Gamemode(self):
    
        # Set the special case for Duels.
        if (self.iPlayers == 2):
            submsg = "[1] Duel\n";
            self.bDuelEnabled = True;
        else:
            submsg = "[1] Deathmatch\n";
    
        msg = "What Gamemode would you like to play?\n"+submsg+"[2] Team Deathmatch\n\
[3] Cooperation\n\
[4] Capture the Flag\n\
[5] Survival\n\
[6] Double Domination\n\
[7] King of the Hill";
        
        self.gamemode = self.common.ClampQuestion(1, 7, msg, "Please input your choice");
        
        # Special case for lives.
        if (self.gamemode == GAMEMODE_SURV):
            self.maxlives = self.common.ClampQuestion(1, 25, msg, "How many lives would you like to have per player?");
 
    def ASK_Difficulty(self):
        
        if (self.gamemode == GAMEMODE_COOP or self.gamemode == GAMEMODE_SURV):
        
            msg = "What Difficulty do you want to have?\n\
[1] I'm too young to die. (Easy+2x ammo)\n\
[2] Hey, not too rough. (Easy)\n\
[3] Hurt me plenty (Normal)\n\
[4] Ultra-Violence (Hard)\n\
[5] NIGHTMARE! (Hard+Fast monsters+ monsters respawn+2x ammo)";
        
            iChoice = self.common.ClampQuestion(1, 5, msg, "What difficulty will the server have?");
            self.skill = iChoice; 
        else:
            self.skill = 5; #Automatically Nightmare for PvP servers.
    ###
    # ASK_BasicInfo 
    # Asks to input the gamemode chosen.
    ###   
    def ASK_DMFlags(self):
      
        if (self.gamemode == GAMEMODE_CTF):
            print ("[INFO] Auto-Applying correct CTF DMFlags.")
            self.dmflags = 17060932;
            self.dmflags2 = 131080;
            return;
    
    
        msg = "What DMFlags are you going to use?\n";
        for i in range (1, len(self.tDmFlagsGamemode[0])+1):
            msg = msg + self.tDmFlagsGamemode[0][i-1]['name']+"\n";
        
        iChoice = self.common.ClampQuestion(1, len(self.tDmFlagsGamemode[iMode])+1, msg, "Please input your choice");
        
        self.iPlayers = self.common.ClampQuestion(2, self.iClients, "", "How many players?");
    
    def ASK_ClientInfo(self):
        self.iClients = self.common.ClampQuestion(2, 100, "", "How many clients would join the server?");
        self.iPlayers = self.common.ClampQuestion(2, self.iClients, "", "How many players?");
    
    def WriteCFG(self):
        
        f = open(filename+ext, 'w')
        f.write ("// Zdaemon Configuration file for " + self.common.Hostname+"\n");
        f.write ("// Creation date: "+now.strftime("%d/%m/%y")+"\n"); #ToDo
        f.write ("// IWAD: " + self.common.IWAD+"\n");
        if (self.common.PWAD):
            f.write ("// PWAD(s): "+ self.common.PWAD+"\n") #Case if we host PWADs
        f.write ("// Generated by Ch0wW's Doom Server Generator - https://github.com/Ch0wW\n");
        
        f.write ("\n");
        f.write ("//------------\n");
        f.write ("// General Server Informations\n");
        f.write ("//------------\n");
        f.write ('set hostname "'+self.common.Hostname+'"\n')
        f.write ('set website "'+self.common.WWWURL+'"\n')
        f.write ('set email "'+self.common.Mail+'"\n')
        f.write ('set motd "" // Please set your MOTD (reminder: <br> goes to a new line\n');
        f.write ("\n");
        f.write ('set password "'+self.common.Password+'"\n')
        f.write ('set join_password "'+self.common.JoinPassword+'"\n')
        f.write ("\n");
        f.write ("//------------\n");
        f.write ("// General Server Settings\n");
        f.write ("//------------\n");
        f.write ('set maxclients "'+str(self.iClients)+'"\n')
        f.write ('set maxplayers "'+str(self.iPlayers)+'"\n')
        f.write ('set gametype "'+str(self.gamemode-1)+'" // '+self.Gamemode_Name(self.gamemode)+"\n");
        f.write ('set skill "'+str(self.skill)+'"\n');
        f.write ("\n");       
        f.write ("//------------\n");
        f.write ("// DMFLAGS\n");
        f.write ("//------------\n");
        f.write ('set dmflags "'+str(self.dmflags)+'"\n')
        f.write ('set dmflags2 "'+str(self.dmflags2)+'"\n')
        f.write ("\n");       
        f.write ("//------------\n");
        f.write ("// Maplist\n");
        f.write ("//------------\n");       
        
    def Run(self):
#        self.common.ASK_IWAD();
#        self.common.ASK_Hostname();
#        self.common.ASK_MailAddress();
#        self.common.ASK_WebAddress();
#        self.common.ASK_Password();
        
        self.ASK_ClientInfo();
        
        # Select Gamemode (and difficulty)
        self.ASK_Gamemode();
        self.ASK_Difficulty();
        
        self.ASK_DMFlags()
        
        # Printing our server.
        print ("=========================================");
        print (" - Server Infos - ");
        print ("► IWAD / PWADs: "+ self.common.IWAD + " / " + self.common.PWAD);
        print ("► Hostname: " + self.common.Hostname);    
        print ("► Contact Mail: "+ self.common.Mail);
        print ('► Password / JoinPassword: "'+ self.common.Password + '" / "' + self.common.JoinPassword+'"');
        print ("► DL Website: "+ self.common.WWWURL);
        print ("");
        print ("► Clients / Players: "+ str(self.iClients) + " / " + str(self.iPlayers));
        print ("");
        print ("► Gamemode: " + self.Gamemode_Name(self.gamemode))
        print ("► Skill: " + str(self.skill))
        print ("=========================================");