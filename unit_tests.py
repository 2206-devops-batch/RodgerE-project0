import shutil
import unittest, os
from util import SaveGame, GameLoop, player_stats, monster_stats, input_output_handler
from unittest.mock import patch
from io import StringIO
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
        self.assertTrue(player.current_action in ("fleeing-success", 'fleeing-fail'))
    
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

class Test_input_output_handler(unittest.TestCase):
    def test_player_name_catch(self):
        # if player did not pass a name arg
        with patch('builtins.input', return_value='Testx'):
            player_name = input_output_handler.player_name_catch('', False)
        self.assertEqual(player_name, "Testx")
        # if player passed a name arg and not logged in
        self.assertEqual(input_output_handler.player_name_catch("['Testy']", False), 'Testy')
        # if player name passed in and logged in
        self.assertEqual(input_output_handler.player_name_catch('Testz', True), 'Testz')
        
    def test_initial_encounter_text(self):
        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.intial_encounter_text()
        flavor_text = ["\nA monster has appeared!\n", "\nA beserk kappa appears!\n", "\nA golem blocks the way!\n", "\nA stray Kobold brandishes a knife!\n", "\nA slime slithers in your way!\n"]
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertTrue(dummy_ouput in flavor_text)
    
    def test_combat_end_text(self):
        # Test each of the 4 situation outcomes
        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.combat_end_text(1)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, "\nIt's a draw! Game Over!")

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.combat_end_text(2)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, "\nYou fall to the ground, broken and battered. Unable to continue on.\n\tGame Over!")

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.combat_end_text(3)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, "\nYour assilant falls into a crumpled mess, defeated. \n\tCongratulations, you are victorious!")

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.combat_end_text(4)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, "\nYou run away from your foe, hopeful to fight another day.")

    def test_end_prompt(self):
        with patch('builtins.input', return_value='pLAy'):
            self.assertTrue(input_output_handler.end_prompt(0, 0))
        with patch('builtins.input', return_value='eXiT '):
            self.assertFalse(input_output_handler.end_prompt(0, 0))

    def test_planning_input(self):
        with patch('builtins.input', return_value='aTtaCk '):
            self.assertEqual(input_output_handler.planning_input(), 'attack')
        with patch('builtins.input', return_value='DefeNd'):
            self.assertEqual(input_output_handler.planning_input(), 'defend')
        with patch('builtins.input', return_value='flEe'):
            self.assertEqual(input_output_handler.planning_input(), 'flee')

    def test_damage_text(self):
        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.damage_text('player', 0, 1)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, 'Seeing an opportunity, you swing at the monster and deal a sizable blow of 0 damage.\n')

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.damage_text('player', 0, 2)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, 'You thrust at the monster with your weapon, but it was prepared for your strike and gets by with only a glancing strike. You deal 0 damage.\n')

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.damage_text('monster', 0, 1)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, "The monster sees its opportunity and lunges at you, dealing 0 damage.\n")

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.damage_text('monster', 0, 2)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, 'The monster visciously lashes out! Dealing 0 damage.\n')

        with patch('sys.stdout', new = StringIO()) as dummy_ouput:
            input_output_handler.damage_text('eh', 0, 4)
        dummy_ouput = dummy_ouput.getvalue()
        dummy_ouput = dummy_ouput[:-1]
        self.assertEqual(dummy_ouput, "You both are locked in a standoff, unwilling to budge.\n")

if __name__ == '__main__':
    unittest.main()
