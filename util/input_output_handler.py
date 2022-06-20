import random
from util import player_stats
def player_name_catch(player_name, logged_in):
    # if player name is empty then prompt user for name
    if not player_name:
        player_name = input("Please enter your player name: ")
    elif not logged_in:
        # clean the input if passed as argv
        player_name = str(player_name)
        player_name = player_name[2:-2]
    return player_name

def intial_encounter_text():
    # modular way of adding more kinds of intial flavor text
    flavor_text = ["\nA monster has appeared!\n", "\nA beserk kappa appears!\n", "\nA golem blocks the way!\n", "\nA stray Kobold brandishes a knife!\n", "\nA slime slithers in your way!\n"]
    x = random.randint(0, (len(flavor_text)-1))
    print(flavor_text[x])    

def combat_end_text(situation):
    if situation == 1:
        print("\nIt's a draw! Game Over!")
    elif situation == 2:
        print("\nYou fall to the ground, broken and battered. Unable to continue on.\n\tGame Over!")
    elif situation == 3:
        print("\nYour assilant falls into a crumpled mess, defeated. \n\tCongratulations, you are victorious!")
    elif situation == 4:
        print("\nYou run away from your foe, hopeful to fight another day.")

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

def planning_input():
    valid_input = False
    while not valid_input:
        player_action = input('How will you proceed? \n\tAttack, Defend, or Flee: ').lower().rstrip()
        for action in player_stats.player.avail_actions:
            if action == player_action:
                valid_input = True
                break
    return player_action

def damage_text(character, dmg, situation):
    if character == 'player' and situation == 1:
        print(f'Seeing an opportunity, you swing at the monster and deal a sizable blow of {dmg} damage.\n')
    elif character == 'player' and situation == 2:
        print(f'You thrust at the monster with your weapon, but it was prepared for your strike and gets by with only a glancing strike. You deal {dmg} damage.\n')
    elif character == 'monster' and situation == 1:
        print(f"The monster sees its opportunity and lunges at you, dealing {dmg} damage.\n")
    elif character == 'monster' and situation == 2:
        print(f'The monster visciously lashes out! Dealing {dmg} damage.\n')
    elif situation == 4:
        print("You both are locked in a standoff, unwilling to budge.\n")

