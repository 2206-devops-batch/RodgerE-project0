def planning_phase(player_char, monster_char):
    # prompts user for their action
    # calls for monster's action, maybe a rng
    # after setting the board passes to combat
    # print('How will you proceed? \n\n\tAttack, Defend, Spells, or Flee: ')
    valid_input = False
    
    while not valid_input:
        player_action = input('How will you proceed? \n\tAttack, Defend, or Flee: ').lower().rstrip()
        for action in player_char.avail_actions:
            if action == player_action:
                valid_input = True
                break

    if player_action == 'attack':
        player_char.set_attacking()
    elif player_action == 'defend':
        player_char.set_attacking()
    elif player_action == 'flee':
        player_char.attempt_flee()

    # else:
    #     print("Please select an available option. \n\n\tAttack, Defend, Spells, or Flee: ")
    #     player_action = input('How will you proceed? \n\n\tAttack, Defend, Spells, or Flee: ').lower().rstrip()

    # what will the monster do?
    monster_char.monster_behavior()

def combat_phase(player_char, monster_char):
    # strength stat vs hp if not defending
    # strength stat vs armor stat with overflow vs hp if defending

    # player will always move first in this demo but a speed stat may be implemented
    pAction = player_char.current_action
    mAction = monster_char.current_action

    # player's combat
    if pAction == 'attacking' and mAction == 'attacking':
        monster_char.hp = monster_char.hp - player_char.strength
        print(f'Seeing an opportunity, you swing at the monster and deal a sizable blow of {player_char.strength} damage.\n')
    elif pAction == 'attacking' and mAction == 'defending':
        if monster_char.armor < player_char.strength:
            damage = player_char.strength - monster_char.armor
        else:
            damage = 0 # if armor > strength then damage to hp is 0
        monster_char.hp = monster_char.hp - damage
        print(f'You thrust at the monster with your weapon, but it was prepared for your strike and gets by with only a glancing strike. You deal {damage} damage.\n')
    elif pAction == 'fleeing-success':
            return #break combat

    # monster's combat
    if (pAction == 'attacking' or pAction == "fleeing-fail") and mAction == 'attacking':
        player_char.hp = player_char.hp - monster_char.strength
        print(f"The monster sees its opportunity and lunges at you, dealing {monster_char.strength} damage.")
    elif mAction == 'attacking' and pAction == 'defending':
        if player_char.armor < monster_char.strength:
            damage = monster_char.strength - player_char.armor
        else:
            damage = 0 # if armor > strength then damage to hp is 0
        player_char.hp = player_char.hp - damage
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
