import os
def create_save_game(player_name):
    # create a new save if the file does not exist
    try:
        player_file = open(f'Save Files/{player_name}.txt', 'x' )
        player_file.write(f"{player_name}, 0, 0")
        player_file.close()
    except FileExistsError:
        pass
    
def get_monsters_defeated(player_name):
    player_file = open(f'Save Files/{player_name}.txt', 'r' )
    save_info = player_file.read().split(', ')
    player_file.close()

    return int(save_info[1])

def get_deaths(player_name):
    player_file = open(f'Save Files/{player_name}.txt', 'r' )
    save_info = player_file.read().split(', ')
    player_file.close()

    return int(save_info[2])

def overwrite_save(player_name, w, l):
    player_file = open(f'Save Files/{player_name}.txt', 'w' )
    player_file.write(f"{player_name}, {w}, {l}")
    player_file.close()
    