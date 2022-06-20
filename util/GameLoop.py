from util.input_output_handler import damage_text, planning_input

def planning_phase(player_char, monster_char):
    # prompts user for their action
    # calls for monster's action, maybe a rng
    # after setting the board passes to combat
    # what will the player do?
    player_action = planning_input()
    if player_action == 'attack':
        player_char.set_attacking()
    elif player_action == 'defend':
        player_char.set_defending()
    elif player_action == 'flee':
        player_char.attempt_flee()

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
        damage_text('player', player_char.strength, 1)
    elif pAction == 'attacking' and mAction == 'defending':
        if monster_char.armor < player_char.strength:
            damage = player_char.strength - monster_char.armor
        else:
            damage = 0 # if armor > strength then damage to hp is 0
        monster_char.hp = monster_char.hp - damage
        damage_text('player', damage, 2)
    elif pAction == 'fleeing-success':
            return #break combat

    # monster's combat
    if (pAction == 'attacking' or pAction == "fleeing-fail") and mAction == 'attacking':
        player_char.hp = player_char.hp - monster_char.strength
        damage_text('monster', monster_char.strength, 1)
    elif mAction == 'attacking' and pAction == 'defending':
        if player_char.armor < monster_char.strength:
            damage = monster_char.strength - player_char.armor
        else:
            damage = 0 # if armor > strength then damage to hp is 0
        player_char.hp = player_char.hp - damage
        damage_text('monster', damage, 2)

    # if both characters choose defend
    if pAction == 'defending' and mAction == 'defending':
        damage_text('none', 0, 4)
