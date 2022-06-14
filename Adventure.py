import sys
from util import GameLoop
from util import SaveGame

def main(player_name, logged_in):
    # character defaults
    player_stats = {'hp': 20, 'strength': 4, 'armor': 5, 'avail_actions': ("attack", "defend", "flee"), 'current action': 'attacking'}
    monster_stats = {'hp': GameLoop.random.randint(1,5), 'strength': GameLoop.random.randint(6,9), 'armor': GameLoop.random.randint(1,3), 'avail_actions': ("attack", "defend"), 'current action': 'attacking'}

    if not player_name:
        player_name = input("Please enter your player name: ")
    elif not logged_in:
        # clean the input
        player_name = str(player_name)
        player_name = player_name[2:-2]
    
    SaveGame.create_save_game(player_name)
    # save file confirmed to exist now

    logged_in = True
    monster_defeated = SaveGame.get_monsters_defeated(player_name)
    deaths = SaveGame.get_deaths(player_name)

    # begin game loop
    # The driver, this will keep the turns going until 1 or both character have hp >= 0
    continue_combat = True

    while continue_combat:
        GameLoop.planning_phase(player_stats, monster_stats)
        GameLoop.combat_phase(player_stats, monster_stats)
        # after combat ends, we'll need to record the outcome too.
        if player_stats['hp'] <= 0 and monster_stats['hp'] <= 0:
            print("\nIt's a draw! Game Over!")
            # add to monsters_defeated and deaths. Then overwrite save
            monster_defeated += 1
            deaths += 1
            SaveGame.overwrite_save(player_name, monster_defeated, deaths)
            continue_combat = False
        elif player_stats['hp'] <= 0:
            print("\nYou fall to the ground, broken and battered. Unable to continue on.\n\tGame Over!")
            # add to deaths. Then overwrite save
            deaths += 1
            SaveGame.overwrite_save(player_name, monster_defeated, deaths)
            continue_combat = False
        elif monster_stats['hp'] <= 0:
            # add to monsters_defeated. Then overwrite save
            print("\nThe monster falls into a crumpled mess, defeated. \n\tCongratulations, you are victorious!")
            monster_defeated += 1
            SaveGame.overwrite_save(player_name, monster_defeated, deaths)
            continue_combat = False
        elif player_stats['current action'] == 'fleeing-success':
            continue_combat = False
    
    # provide an option to check win/loss record and exit -or- play another combat
    if GameLoop.end_prompt(monster_defeated, deaths):
        main(player_name, logged_in=True)
    
if __name__ == "__main__":
    main(sys.argv[1:], False)
