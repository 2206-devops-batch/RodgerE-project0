import random
# character defaults
player_stats = {'hp': 10, 'strength': 2, 'armor': 4, 'avail_actions': ("attack", "defend", "flee"), 'current action': 'attacking'} # an observe action may be fun
monster_stats = {'hp': 5, 'strength': 5, 'armor': 1, 'avail_actions': ("attack", "defend"), 'current action': 'attacking'}

def set_attacking(activeCharacter):
    # sets the current character's current action to 'attacking'
    if activeCharacter == 'Player':
        player_stats['current action'] = 'attacking'
    elif activeCharacter == 'Monster':
        monster_stats['current action'] = 'attacking'
    

def set_defending(activeCharacter):
    # sets the current character's current action to 'defending'
    if activeCharacter == 'Player':
        player_stats['current action'] = 'defending'
    elif activeCharacter == 'Monster':
        monster_stats['current action'] = 'defending'

def monster_behavior():
    coin_toss = random.randint(1,2)
    if coin_toss == 1:
        set_attacking('Monster')
    else:
        set_defending('Monster')

def planning_phase():
    # prompts user for their action
    # calls for monster's action, maybe a rng
    # after setting the board passes to combat
    # print('How will you proceed? \n\n\tAttack, Defend, Spells, or Flee: ')
    valid_input = False
    
    while not valid_input:
        player_action = input('How will you proceed? \n\n\tAttack, Defend, or Flee: ').lower().rstrip()
        for action in player_stats['avail_actions']:
            if action == player_action:
                valid_input = True
                break

    if player_action == 'attack':
        set_attacking('Player')
    elif player_action == 'defend':
        set_defending('Player')
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
    monster_behavior()

    pass

def combat_phase():
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

def main():
    # The driver, this will keep the turns going until 1 or both character have hp >= 0
    continue_combat = True

    while continue_combat:
        planning_phase()
        combat_phase()
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
    pass

main()
