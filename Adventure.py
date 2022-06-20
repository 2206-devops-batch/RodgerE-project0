import sys
from util import GameLoop, SaveGame, player_stats, monster_stats, input_output_handler

def main(player_name, logged_in):
    # character init
    player_character = player_stats.player()
    monster_character = monster_stats.monster()

    # player name must be filled for save file
    player_name = input_output_handler.player_name_catch(player_name, logged_in)
    SaveGame.create_save_game(player_name)
    # save file confirmed to exist now

    # prevents from truncating the name if player chooses to play again without exiting
    logged_in = True

    monster_defeated = SaveGame.get_monsters_defeated(player_name)
    deaths = SaveGame.get_deaths(player_name)

    # begin game loop
    # The driver, this will keep the turns going until 1 or both character have hp >= 0
    continue_combat = True
    input_output_handler.intial_encounter_text()
    while continue_combat:
        GameLoop.planning_phase(player_character, monster_character)
        GameLoop.combat_phase(player_character, monster_character)
        # after combat ends, we'll need to record the outcome too.
        if player_character.hp <= 0 and monster_character.hp <= 0:
            input_output_handler.combat_end_text(1)
            # add to monsters_defeated and deaths. Then overwrite save
            monster_defeated += 1
            deaths += 1
            SaveGame.overwrite_save(player_name, monster_defeated, deaths)
            continue_combat = False
        elif player_character.hp <= 0:
            input_output_handler.combat_end_text(2)
            # add to deaths. Then overwrite save
            deaths += 1
            SaveGame.overwrite_save(player_name, monster_defeated, deaths)
            continue_combat = False
        elif monster_character.hp <= 0:
            input_output_handler.combat_end_text(3)
            # add to monsters_defeated. Then overwrite save
            monster_defeated += 1
            SaveGame.overwrite_save(player_name, monster_defeated, deaths)
            continue_combat = False
        elif player_character.current_action == 'fleeing-success':
            input_output_handler.combat_end_text(4)
            continue_combat = False
    
    # provide an option to check win/loss record and exit -or- play another combat
    if input_output_handler.end_prompt(monster_defeated, deaths):
        main(player_name, logged_in=True)
    
if __name__ == "__main__":
    main(sys.argv[1:], False)
