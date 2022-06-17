import shutil
import unittest, os
from util import SaveGame

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

    def test_set_attacking(self):
        pass
    
    def test_set_defending(self):
        pass

    def test_monster_behavior(self):
        pass
    
    def test_planning_phase(self):
        pass

    def test_combat_phase(self):
        pass

    def test_end_prompt(self):
        pass

class Test_Adventure(unittest.TestCase):

    def test_main(self):
        pass


if __name__ == '__main__':
    unittest.main()
