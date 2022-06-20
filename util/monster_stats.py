import random
class monster:
    # monster_stats = {'hp': GameLoop.random.randint(1,5), 'strength': GameLoop.random.randint(6,9), 'armor': GameLoop.random.randint(1,3), 'avail_actions': ("attack", "defend"), 'current action': 'attacking'}
    hp = random.randint(1,5)
    strength = random.randint(6,9)
    armor = random.randint(1,3)
    avail_actions = ("attack", "defend")
    current_action = 'attacking'
    
    def set_attacking(self):
    # sets the current character's current action to 'attacking'
        self.current_action = 'attacking'

    def set_defending(self):
    # sets the current character's current action to 'attacking'
        self.current_action = 'defending'

    def monster_behavior(self):
        if random.randint(1, 100)> 60:
            self.set_attacking
        else:
            self.set_defending