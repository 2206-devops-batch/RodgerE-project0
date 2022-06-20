import random
class player:
    # player_stats = {'hp': 20, 'strength': 4, 'armor': 5, 'avail_actions': ("attack", "defend", "flee"), 'current action': 'attacking'}
    # default values
    hp = 20
    strength = 4
    armor = 5
    avail_actions = ("attack", "defend", "flee")
    current_action = "attacking"
    
    def set_attacking(self):
    # sets the current character's current action to 'attacking'
        self.current_action = 'attacking'

    def set_defending(self):
    # sets the current character's current action to 'attacking'
        self.current_action = 'defending'
    
    def attempt_flee(self):
        if random.randint(0, 100) > 80:
            self.current_action = "fleeing-success"
        else:
            self.current_action = "fleeing-fail"