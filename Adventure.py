import sys
from util import GameLoop

def main(argv = ''):
    # character defaults
    player_stats = {'hp': 10, 'strength': 2, 'armor': 4, 'avail_actions': ("attack", "defend", "flee"), 'current action': 'attacking'}
    monster_stats = {'hp': 5, 'strength': 5, 'armor': 1, 'avail_actions': ("attack", "defend"), 'current action': 'attacking'}

    # to include a win loss record, we'll need a save file to work from
    # lets make it a json file for the save files

    # if no player name was given as argv, ask for an existing name or make a new one
    # after a file was made/read, print a setting for the opening encounter
    # begin game loop


    # The driver, this will keep the turns going until 1 or both character have hp >= 0
    continue_combat = True

    while continue_combat:
        GameLoop.planning_phase(player_stats, monster_stats)
        GameLoop.combat_phase(player_stats, monster_stats)
        # after combat ends, we'll need to record the outcome too.
        if player_stats['hp'] <= 0 and monster_stats['hp'] <= 0:
            print("\nIt's a draw! Game Over!")
            continue_combat = False
        elif player_stats['hp'] <= 0:
            print("\nYou fall to the ground, broken and battered. Unable to continue on.\n\tGame Over!")
            continue_combat = False
        elif monster_stats['hp'] <= 0:
            print("\nThe monster falls into a crumpled mess, defeated. \n\tCongratulations, you are victorious!")
            continue_combat = False
        elif player_stats['current action'] == 'fleeing-success':
            continue_combat = False
    
    # provide an option to check win/loss record -or- play another combat -or- exit
    
    pass

if __name__ == "__main__":
   main(sys.argv[1:])
