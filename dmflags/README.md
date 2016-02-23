#Understanding the template:

To gain some time for developping this tool, and to update templates, I used a json system to automatically develop the most optimal settings in fewest lines of code possible.

## Zdaemon

Zdaemon's way to change gamemodes are through a single CVAR, "gamemode". However, a few exceptions can be done:
- Either switching to duel mode (with maxplayers set to 2);
- Selecting Cooperation or Survival: you have to put gamemode to 2 or 4, AND to set cooperative to 1.

The structure is done that way:
{
	"gamemode": 1,
	"duel": 0,
	"cooperative": 0,
	"name": "Oldschool DM (DOOM DOS settings)",
			
	"dmflags": 0,
	"dmflags2": 0, 
	"dmflags3": 0
}

gamemode: the corresponding gamemode. (0: FFA/Duel, 1: TDM, 2: Coop, 3: CTF, 4: Survival, 5: DDOM, 6: KOTH)
duel: if the gamemode is a duel. (set gamemode to 1 too)
cooperative: if the gamemode is a cooperative one. (set gamemode to either 2 or 4)
name: the name publicly seen when using the tool.

dmflags: the dmflags used.
dmflags2: the dmflags2 used. 
dmflags3: the dmflags3 used. 