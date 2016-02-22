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
    tDmFlags = [[] for _ in range (7)];
    iEnableVoice = 0;
    
    def __init__(self, commonclass):
        self.common = commonclass;
        
        # Sort the Zdaemon json file through a local array.
        with open ("dmflags/zdaemon.json") as filename:
            tDmflags = json.load(filename);
            
        for element in tDmflags:            
            # Register allowed values.
            if (element['gamemode'] == 0 and element['duel'] == 1):
                self.tDmFlags[SORT_DUEL].append(element);
            elif (element['gamemode'] == 0 and element['duel'] == 0):
                self.tDmFlags[SORT_FFA].append(element);
            elif (element['gamemode'] == 1):
                self.tDmFlags[SORT_TDM].append(element);
            elif ( (element['gamemode'] == 2 or element['gamemode'] == 4) and element['cooperative'] == 1):
                self.tDmFlags[SORT_COOP].append(element);
            elif (element['gamemode'] == 3):
                self.tDmFlags[SORT_CTF].append(element);
            elif (element['gamemode'] == 5):
                self.tDmFlags[SORT_DDOM].append(element);
            elif (element['gamemode'] == 6):
                self.tDmFlags[SORT_KOTH].append(element);
                
        # ToDo: Is there something cleaner?
        print ("Total of templates: "+str(len(self.tDmFlags[0])+len(self.tDmFlags[1])+len(self.tDmFlags[2])+len(self.tDmFlags[3])+len(self.tDmFlags[4])+len(self.tDmFlags[5])+len(self.tDmFlags[6])))
     
    def ASK_ClientInfo(self):
        self.iClients = self.common.ClampQuestion(2, 100, "", "How many clients would join the server?");
        self.iPlayers = self.common.ClampQuestion(2, self.iClients, "", "How many players?");
        
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
        elif (mode == GAMEMODE_KOTH): return "King of the Hill";
        return "Deathmatch"; #Default Mode
        
    def Gamemode_Short(self, mode):
        if   (mode == GAMEMODE_DM):   return "dm"; 
        elif (mode == GAMEMODE_TDM):  return "tdm";
        elif (mode == GAMEMODE_COOP): return "coop";
        elif (mode == GAMEMODE_CTF):  return "ctf";
        elif (mode == GAMEMODE_SURV): return "surv";
        elif (mode == GAMEMODE_DDOM): return "ddom";
        elif (mode == GAMEMODE_KOTH): return "koth";
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
        
            self.skill = self.common.ClampQuestion(1, 5, msg, "What difficulty will the server have?");
        else:
            self.skill = 5;
    ###
    # ASK_BasicInfo 
    # Asks to input the gamemode chosen.
    ###   
    def ASK_DMFlags(self):
      
        # Have to sort them out. Sucks.
        if (self.bDuelEnabled):
            iMode = SORT_DUEL;
        elif (self.gamemode == GAMEMODE_DM and not self.bDuelEnabled):
            iMode = SORT_FFA;
        elif (self.gamemode == GAMEMODE_TDM):
            iMode = SORT_TDM;
        elif (self.gamemode == GAMEMODE_COOP or self.gamemode == GAMEMODE_SURV):
            iMode = SORT_COOP;
        elif (self.gamemode == GAMEMODE_CTF):
            iMode = SORT_CTF;
        elif (self.gamemode == GAMEMODE_DDOM):
            iMode = SORT_DDOM;
        elif (self.gamemode == GAMEMODE_KOTH):
            iMode = SORT_KOTH;
        
        #Have to sort them from [1]. I know, that sucks even more.
        msg = "What DMFlags are you going to use?\n";
        for i in range (1, len(self.tDmFlags[iMode])+1):
            msg = msg + '['+str(i)+'] '+self.tDmFlags[iMode][i-1]['name']+"\n";
        msg = msg + '['+str(len(self.tDmFlags[iMode])+1)+'] Custom DMFlags (Unsupported)';
        
        iChoice = self.common.ClampQuestion(1, len(self.tDmFlags[iMode]), msg, "Please input your choice"); #ONCE CUSTOM's COMPLETED - MUST BE >>>> len(self.tDmFlags[iMode]+1
        
        if (iChoice == len(self.tDmFlags[iMode])+1):
            print ("We told you it's currently unsupported... Setting DMFlags to 0.");
            self.dmflags  = 0;
            self.dmflags2 = 0;
            self.dmflags3 = 0;
        
        self.dmflags  = self.tDmFlags[iMode][iChoice-1]['dmflags'];
        self.dmflags2 = self.tDmFlags[iMode][iChoice-1]['dmflags2'];
        self.dmflags3 = self.tDmFlags[iMode][iChoice-1]['dmflags3'];
        
        print ("[INFO] Setting DMFLAGS to: "+str(self.dmflags) + " / " + str(self.dmflags2) + " / " + str(self.dmflags3) )
    
    
    def ASK_VoiceSettings(self):
        self.iEnableVoice = self.common.ClampQuestion(0, 1, "", "Would you like to enable voice chat?");
        
    def WriteCFG(self):
        
        now = date.today();
        
        filename = self.Gamemode_Short(self.gamemode)+'_'+self.common.IWAD_Short(self.common.IWADNb)+'_'+now.strftime("%d_%m"); #ToDo: Add too PWADs.
        ext = ".cfg"
        f = open(filename+ext, 'w')
        
        #sudo make me the config
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
        f.write ('set motd "" // Please set your MOTD (reminder: <br> goes to a new line)\n');
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
        
        #DMFLAGS SETTINGS
        f.write ("//------------\n");
        f.write ("// DMFLAGS\n");
        f.write ("//------------\n");
        f.write ('set dmflags "'+str(self.dmflags)+'"\n')
        f.write ('set dmflags2 "'+str(self.dmflags2)+'"\n')
        f.write ('set dmflags3 "'+str(self.dmflags3)+'"\n')
        f.write ("\n");       
        
        #MAPLIST SETTINGS
        f.write ("//------------\n");
        f.write ("// Maplist\n");
        f.write ("//------------\n");
        if (self.common.IWAD == "DOOM.WAD"):
            for i in range (0, 4):
                for y in range (0, 9):
                    f.write('addmap "e'+str(i+1)+'m'+str(y+1)+'"\n');
        else:
            for i in range (0, 15):
                if (i+1 < 10):
                    f.write('addmap "map0'+str(i+1)+'"\n');
                else:
                    f.write('addmap "map'+str(i+1)+'"\n');
            f.write('addmap "map31"\n');
            f.write('addmap "map32"\n');
            
            for i in range (15, 30):
                f.write('addmap "map'+str(i+1)+'"\n');
        f.write ("\n");  
        
        #VOICE SETTINGS
        f.write ("//------------\n");
        f.write ("// Voice Settings\n");
        f.write ("//------------\n");
        f.write ('set sv_voice_chat            "'+str(self.iEnableVoice)+'"\n');
        f.write ('set sv_voice_max_quality     "3"\n')
        f.write ("\n");     
        
        #VOTE SETTINGS 
        # If it's cooperation, don't touch. 
        if (self.gamemode != GAMEMODE_COOP or self.gamemode != GAMEMODE_SURV):
            f.write ("//------------\n");
            f.write ("// Vote Settings\n"); 
            f.write ("//------------\n");
            f.write ('set sv_vote_limit        "3"\n');
            f.write ('set sv_vote_timeout    "120"\n');
            f.write ("\n");    
            f.write ('set sv_vote_reset         "1"\n');  
            f.write ('set sv_vote_randmap       "0"\n');
            f.write ('set sv_vote_map           "0"\n');
            f.write ('set sv_vote_map_percent "100"\n');
            f.write ('set sv_vote_map_skip      "0"\n');
            f.write ("\n"); 		 
            f.write ('set sv_vote_kick          "1"\n'); 
            f.write ('set sv_vote_kick_percent "60"\n');
            f.write ('set sv_vote_min          "51"\n');
            f.write ('set sv_vote_randcaps      "0"');
        f.close();
       
        
    def Run(self):
        self.common.ASK_IWAD();
        self.common.ASK_PWAD();
        self.common.ASK_Hostname();
        self.common.ASK_MailAddress();
        self.common.ASK_WebAddress();
        self.common.ASK_Password();
        
        self.ASK_ClientInfo();
        
        # Select Gamemode (and difficulty)
        self.ASK_Gamemode();
        self.ASK_Difficulty();
        self.ASK_DMFlags()
        self.ASK_VoiceSettings();
        
        self.WriteCFG();
        
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
        print ("► DMFlags: "+str(self.dmflags) + " / " + str(self.dmflags2) + " / " + str(self.dmflags3) )
        print ("=========================================");