import random
def set_attacking(activeCharacter, active_char_stats):
    # sets the current character's current action to 'attacking'
    if activeCharacter == 'Player':
        active_char_stats['current action'] = 'attacking'
    elif activeCharacter == 'Monster':
        active_char_stats['current action'] = 'attacking'
    

def set_defending(activeCharacter, active_char_stats):
    # sets the current character's current action to 'defending'
    if activeCharacter == 'Player':
        active_char_stats['current action'] = 'defending'
    elif activeCharacter == 'Monster':
        active_char_stats['current action'] = 'defending'

def monster_behavior(monster_stats):
    coin_toss = random.randint(1, 100)
    if coin_toss > 40:
        set_attacking('Monster', monster_stats)
    else:
        set_defending('Monster', monster_stats)

def planning_phase(player_stats, monster_stats):
    # prompts user for their action
    # calls for monster's action, maybe a rng
    # after setting the board passes to combat
    # print('How will you proceed? \n\n\tAttack, Defend, Spells, or Flee: ')
    valid_input = False
    
    while not valid_input:
        player_action = input('How will you proceed? \n\tAttack, Defend, or Flee: ').lower().rstrip()
        for action in player_stats['avail_actions']:
            if action == player_action:
                valid_input = True
                break

    if player_action == 'attack':
        set_attacking('Player', player_stats)
    elif player_action == 'defend':
        set_defending('Player', player_stats)
    elif player_action == 'flee':
        if random.randint(0, 100) > 80:
            print("You run for your life, barely getting away from the beast.\n")
            player_stats['current action'] = "fleeing-success"
        else:
            print("You attempt to break away, but the monster blocks your way.\n")
            player_stats['current action'] = "fleeing-fail"
    # else:
    #     print("Please select an available option. \n\n\tAttack, Defend, Spells, or Flee: ")
    #     player_action = input('How will you proceed? \n\n\tAttack, Defend, Spells, or Flee: ').lower().rstrip()

    # what will the monster do?
    monster_behavior(monster_stats)

    pass

def combat_phase(player_stats, monster_stats):
    # strength stat vs hp if not defending
    # strength stat vs armor stat with overflow vs hp if defending

    # player will always move first in this demo but a speed stat may be implemented
    pAction = player_stats['current action']
    mAction = monster_stats['current action']

    # player's combat
    if pAction == 'attacking' and mAction == 'attacking':
        monster_stats['hp'] = monster_stats['hp'] - player_stats['strength']
        print(f'Seeing an opportunity, you swing at the monster and deal a sizable blow of {player_stats["strength"]} damage.\n')
    elif pAction == 'attacking' and mAction == 'defending':
        if monster_stats['armor'] < player_stats['strength']:
            damage = player_stats['strength'] - monster_stats['armor']
        else:
            damage = 0 # if armor > strength then damage to hp is 0
        monster_stats['hp'] = monster_stats['hp'] - damage
        print(f'You thrust at the monster with your weapon, but it was prepared for your strike and gets by with only a glancing strike. You deal {damage} damage.\n')
    elif player_stats['current action'] == 'fleeing-success':
            return #break combat

    # monster's combat
    if (pAction == 'attacking' or pAction == "fleeing-fail") and mAction == 'attacking':
        player_stats['hp'] = player_stats['hp'] - monster_stats['strength']
        print(f"The monster sees its opportunity and lunges at you, dealing {monster_stats['strength']} damage.")
    elif mAction == 'attacking' and pAction == 'defending':
        if player_stats['armor'] < monster_stats['strength']:
            damage = monster_stats['strength'] - player_stats['armor']
        else:
            damage = 0 # if armor > strength then damage to hp is 0
        player_stats['hp'] = player_stats['hp'] - damage
        print(f'The monster visciously lashes out! Dealing {damage} damage.')

    # if both characters choose defend
    if pAction == 'defending' and mAction == 'defending':
        print("You both are locked in a standoff, unwilling to budge.\n")

def end_prompt(monsters_defeated, deaths):
    valid_input = False
    avail_menu_options = ['play', 'play again', 'record','my record', 'exit' ]
    while not valid_input:
        end_menu =input("\nWould like to play again or see your record and exit? ").lower().rstrip()
        for action in avail_menu_options:
            if action == end_menu:
                valid_input = True
                break
    if (end_menu == avail_menu_options[0]) or (end_menu == avail_menu_options[1]):
        return True
    elif (end_menu == avail_menu_options[2]) or (end_menu == avail_menu_options[3]) or (end_menu == avail_menu_options[4]):
        if deaths > 0:
            k_d = monsters_defeated / deaths
        else:
            k_d = monsters_defeated
        print(f"You have {monsters_defeated} monsters defeated and {deaths} deaths. Giving a K/D of {k_d}")
        print("\nThank you for playing!")
        return False
