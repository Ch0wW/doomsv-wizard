#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date;

#=============================
# Zdaemon Class for generating a server.
#=============================
class ChocoDoomServer():

    common = "";
    modifier = "";
    timelimit = "";
    episode = 1;
    level = 1;
    
    def __init__(self, commonclass, platform):
        self.common = commonclass;
        self.platform = platform;
 
    def ASK_Difficulty(self):
        
        if (self.game == 1):
            msg = "What Difficulty would you like to play?\n\
[1] I'm too young to die. (Easy+2x ammo)\n\
[2] Hey, not too rough. (Easy)\n\
[3] Hurt me plenty (Normal)\n\
[4] Ultra-Violence (Hard)\n\
[5] NIGHTMARE! (Hard+Fast monsters+ monsters respawn+2x ammo)";
        
            self.skill = self.common.ClampQuestion(1, 5, msg, "Please input your choice");
        else:
            self.skill = 5; #Automatically Nightmare for PvP servers.
			
        if (self.skill == 5):
            return;
			
        msgsec = "What gameplay modifier would you like to have?\n\
[1] None.\n\
[2] No monsters.\n\
[3] Fast monsters.\n\
[4] Respawning monsters\n\
[5] Fast + Respawning monsters.";
		
        iChoice = self.common.ClampQuestion(1, 5, msgsec, "Please input your choice");
		
        if (iChoice == 1):
            return;
        elif (iChoice == 2):
            self.modifier = "-nomonsters";
        elif (iChoice == 3):
            self.modifier = "-fast";
        elif (iChoice == 4):
            self.modifier = "-respawn";
        elif (iChoice == 5):
            if (self.skill == 4):
                print ("[INFO] I'm setting your game on Nightmare! skill instead.");
                self.skill = 5;
            else:
                self.modifier == "-fast -nomonsters";
	
    def Get_GamemodeName(self, mode):
        if (mode == 1): return "Cooperation";
        elif (mode == 2): return "Deathmatch";
        elif (mode == 3): return "Alt. Deathmatch";
    
    def ASK_Gamemode(self):
        
        msg = "What Gamemode would you like to play?\n\
[1] Cooperation\n\
[2] Deathmatch (No item respawn)\n\
[3] Alt. Deathmatch (everything respawn after 30 secs)";
        
        iChoice = self.common.ClampQuestion(1, 3, msg, "Please input your choice");
        self.game = iChoice; 
			
        if (self.game == 1):
            self.gamemode = "";
        elif (self.game == 2):
            self.gamemode = "-deathmatch";
        else:
            self.gamemode = "-altdeath";
    ###
    # ASK_BasicInfo 
    # Asks to input the gamemode chosen.
    ###   
    def ASK_ClientInfo(self):
        self.iClients = self.common.ClampQuestion(2, 4, "", "How many clients would join the server?");
    
    ###
    # ASK_TimeLimit
    # Asks to input the gamemode chosen.
    ###   	
    def ASK_Timelimit(self):
        if (self.game == 1):
            return;
			
        self.time = self.common.ClampQuestion(0, 60, "", "Do you want to set a timelimit? (0 cancels, 20 is AVG)");
		
        if (self.time == 0):
            self.timelimit = "";
        elif (self.time == 20):
            print ("[INFO] I'm setting the timelimit from Austin Virtual Gaming official settings.");
            self.timelimit = " -avg";
        else:
            self.timelimit = " -timer "+str(self.time);
	
    def ASK_EpisodeLevel(self):
        if (self.common.IWAD == "DOOM.WAD"):
            msg = "On what episode would you like to play?\n\
[1] Episode 1\n\
[2] Episode 2\n\
[3] Episode 3\n\
[4] Episode 4";
        
            self.episode = self.common.ClampQuestion(1, 4, msg, "Please input your choice"); 
            self.level = self.common.ClampQuestion(1, 9, "", "What level from the episode would you like to play?");
    
        else:
            self.level = self.common.ClampQuestion(1, 32, "", "What level would you like to play?");      
            
    def ASK_Port(self):
        msg = "Finally, will you play on Chocolate Doom, or the good ol' DOS version (through DosBox)?\n\
[1] Chocolate Doom\n\
[2] Doom DOS";
        self.port = self.common.ClampQuestion(1, 2, msg, "Please input your choice");    
    
    def WriteCFG(self, filename, port, platform):
        
        params = "";
        
        if (platform == "Windows" or self.port == 2):
            ext = ".bat";
            iPlatform = 0;
        else:
            ext = ".sh"
            iPlatform = 1;
            
        f = open(filename+ext, 'w');
        
        # Set the headers.
        if (self.port == 2):
            f.write ("::##################################\n");
            f.write ("::# Server Configuration file for DOSBox / Doom DOS\n");
            f.write ("::# Creation date: "+date.today().strftime("%d/%m/%y")+"\n"); #ToDo: date()
            f.write ("::# IWAD: " + self.common.IWAD+"\n");
            if (self.common.PWAD):
                f.write ("::# PWAD(s): "+ self.common.PWAD+"\n") #Case if we host PWADs
            f.write ("::# \n");
            f.write ("::# Generated by Ch0wW's Doom Server tool - http://ch0ww.baseq.fr"+"\n");
            f.write ("::##################################\n");
            f.write ("\n");
        else:
            f.write (self.common.ReplaceOS(iPlatform, "#==================================\n"));
            f.write (self.common.ReplaceOS(iPlatform, "# Server Configuration file for Chocolare Doom\n"));
            f.write (self.common.ReplaceOS(iPlatform, "# Creation date: "+date.today().strftime("%d/%m/%y")+"\n")); #ToDo: date()
            f.write (self.common.ReplaceOS(iPlatform, "# IWAD: " + self.common.IWAD+"\n"));
            if (self.common.PWAD):
                f.write (self.common.ReplaceOS(iPlatform, "# PWAD(s): "+ self.common.PWAD+"\n")) #Case if we host PWADs
            f.write (self.common.ReplaceOS(iPlatform, "# Don't forget to open port 5080 UDP if you plan to play online!\n"));
            f.write (self.common.ReplaceOS(iPlatform, "# \n"));
            f.write (self.common.ReplaceOS(iPlatform, "# Generated by Ch0wW's Doom Server tool - http://ch0ww.baseq.fr"+"\n"));
            f.write (self.common.ReplaceOS(iPlatform, "#==================================\n"));
            f.write ("\n");
            
        # Apply parameters.
        if (self.port == 1):
            params = "-iwad "+self.common.IWAD;
        if (self.common.PWAD):
            params = (params + " -file "+self.common.PWAD);
        if (self.iClients > 2):
            params = (params + " -nodes "+str(self.iClients));
        if (self.skill != 3):
            params = params + " -skill " +str(self.skill);
        if (self.gamemode):
            params = (params + " " +self.gamemode);
        if (self.modifier):
            params = (params + " " +self.modifier);
        if (self.episode > 1 and self.level > 1):
            params = (params + " -warp " +str(self.episode)+" "+str(self.level));
        elif (self.level > 1):
            params = (params + " -warp " +str(self.level));
        if (self.time):
            params = (params +self.timelimit);    
            
        # Don't mess with it. Write both instead!
        if (self.port == 1):          f.write ("./chocolate-doom "+params+" -port 2342\n");
        else:                         f.write ("./IPXSETUP.EXE "+params);
        
        f.close();
                
    def Run(self):
        self.common.ASK_IWAD();
      
        self.ASK_ClientInfo();
        
        # Select Gamemode (and difficulty)
        self.ASK_Gamemode();
        self.ASK_Difficulty();
        
        self.ASK_Timelimit()
        self.ASK_EpisodeLevel();
        
        self.ASK_Port();
        
        if (self.port == 1):
            self.WriteCFG("Chocodoom_Server", self.port, self.platform);
        else:
            self.WriteCFG("doomdosv", self.port, self.platform);
        
        # Printing our server.
        print ("=========================================");
        print (" - Server Infos - ");
        print ("► IWAD / PWADs: "+ self.common.IWAD + " / " + self.common.PWAD);
        print ("");
        print ("► Clients required: "+ str(self.iClients));
        print ("");
        print ("► Gamemode: " + self.Get_GamemodeName(self.game))
        print ("► Skill: " + str(self.skill))
        print ("► Timelimit: " + str(self.time))
        print ("=========================================");