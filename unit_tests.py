import shutil
import unittest, os
from util import SaveGame, GameLoop, player_stats, monster_stats, input_output_handler
from unittest.mock import patch
class Test_Save_Game(unittest.TestCase):

    def test_create_save_game(self):
        # test creation of new file
        if os.path.exists("Save_Files/tester.txt"):
            os.remove("Save_Files/tester.txt")
        SaveGame.create_save_game("tester")
        file_test = open('Save_Files/tester.txt', 'r' )
        line = file_test.read()
        file_test.close()
        self.assertEqual(line, 'tester, 0, 0')
        # test that file creation does not edit existing file
        file_test = open('Save_Files/tester.txt', 'w' )
        line = file_test.write("tester, 7, 7")
        file_test.close()
        SaveGame.create_save_game('tester')
        self.assertEqual(SaveGame.get_monsters_defeated("tester"), 7)
        self.assertEqual(SaveGame.get_deaths("tester"), 7)
        # test that if a Save_Files dir does not exist, that one is made
        shutil.rmtree("Save_Files") #remove dir and its files
        SaveGame.create_save_game("tester")
        self.assertTrue(os.path.exists('Save_Files/tester.txt'))

    def test_get_monsters_defeated(self):
        if os.path.exists("Save_Files/tester.txt"):
            os.remove("Save_Files/tester.txt")
        SaveGame.create_save_game("tester")
        self.assertEqual(SaveGame.get_monsters_defeated("tester"), 0)

    def test_get_deaths_defeated(self):
        if os.path.exists("Save_Files/tester.txt"):
            os.remove("Save_Files/tester.txt")
        SaveGame.create_save_game("tester")
        self.assertEqual(SaveGame.get_deaths("tester"), 0)
    
    def test_overwrite_save(self):
        if os.path.exists("Save_Files/tester.txt"):
            os.remove("Save_Files/tester.txt")
        SaveGame.create_save_game("tester")
        deaths = SaveGame.get_deaths("tester")
        monsters_d = SaveGame.get_monsters_defeated("tester")
        self.assertEqual(deaths, 0)
        self.assertEqual(monsters_d, 0)
        SaveGame.overwrite_save("tester", 67, 24)
        self.assertEqual(SaveGame.get_monsters_defeated("tester"), 67)
        self.assertEqual(SaveGame.get_deaths("tester"), 24)

class Test_GameLoop(unittest.TestCase):

    def test_planning_phase(self):
        player = player_stats.player()
        monster = monster_stats.monster()
        # player chooses attack
        with patch('builtins.input', return_value='attack'):
            GameLoop.planning_phase(player, monster)
        self.assertEqual(player.current_action, "attacking")
        # player chooses defend
        with patch('builtins.input', return_value='defend'):
            GameLoop.planning_phase(player, monster)
        self.assertEqual(player.current_action, "defending")
        # player chooses flee
        with patch('builtins.input', return_value='flee'):
            GameLoop.planning_phase(player, monster)
        self.assertTrue(player.current_action, ("fleeing-success" or 'fleeing-fail'))

    def test_combat_phase(self):
        player = player_stats.player()
        monster = monster_stats.monster()
        monster_old_hp = monster.hp
        # if both are attacking
        GameLoop.combat_phase(player, monster)
        self.assertNotEqual(player.hp, 20)
        self.assertNotEqual(monster.hp, monster_old_hp)

        player = player_stats.player()
        monster = monster_stats.monster()
        monster_old_hp = monster.hp
        # If player attacks but monster defends
        monster.current_action = 'defending'
        GameLoop.combat_phase(player, monster)
        self.assertEqual(player.hp, 20)
        self.assertNotEqual(monster.hp, monster_old_hp)

        player = player_stats.player()
        monster = monster_stats.monster()
        monster_old_hp = monster.hp
        # if player defends but monster attacks
        player.current_action = 'defending'
        GameLoop.combat_phase(player, monster)
        self.assertNotEqual(player.hp, 20)
        self.assertEqual(monster.hp, monster_old_hp)

        player = player_stats.player()
        monster = monster_stats.monster()
        monster_old_hp = monster.hp
        # if both choose defend
        player.current_action = 'defending'
        monster.current_action = 'defending'
        GameLoop.combat_phase(player, monster)
        self.assertEqual(player.hp, 20)
        self.assertEqual(monster.hp, monster_old_hp)

class Test_Adventure(unittest.TestCase):

    def test_main(self):
        pass


if __name__ == '__main__':
    unittest.main()
