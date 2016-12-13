from shutil import rmtree
import unittest
import epub_cleaner
import os.path

class TestCleanInit(unittest.TestCase):
    def test_simple(self):
        tmp = epub_cleaner.EpubCleaner('Dracula.epub')
        self.assertEqual(tmp.old_epub_name, 'Dracula.epub')
        self.assertEqual(tmp.old_dir_name, 'Dracula')
        self.assertEqual(tmp.new_epub_name, 'clean_Dracula.epub')
        self.assertEqual(tmp.new_dir_name, 'clean_Dracula')

    def test_absolute(self):
        tmp = epub_cleaner.EpubCleaner('/home/nate/Dracula.epub')
        self.assertEqual(tmp.old_epub_name, '/home/nate/Dracula.epub')
        self.assertEqual(tmp.old_dir_name, '/home/nate/Dracula')
        self.assertEqual(tmp.new_epub_name, '/home/nate/clean_Dracula.epub')
        self.assertEqual(tmp.new_dir_name, '/home/nate/clean_Dracula')

    def test_relative(self):
        tmp = epub_cleaner.EpubCleaner('/../Dracula.epub')
        self.assertEqual(tmp.old_epub_name, '/../Dracula.epub')
        self.assertEqual(tmp.old_dir_name, '/../Dracula')
        self.assertEqual(tmp.new_epub_name, '/../clean_Dracula.epub')
        self.assertEqual(tmp.new_dir_name, '/../clean_Dracula')

class TestCleanSetup(unittest.TestCase):
    def test_simple(self):
        tmp = epub_cleaner.EpubCleaner('test/HenryVI.epub')
        tmp.setup()
        self.assertTrue(os.path.exists('test/HenryVI'))
        self.assertTrue(os.path.exists('test/clean_HenryVI'))
        self.assertFalse(os.path.isfile('test/HenryVI'))
        self.assertFalse(os.path.isfile('test/clean_HenryVI'))

    def tearDown(self):
        rmtree('test/HenryVI')
        rmtree('test/clean_HenryVI')

class TestCleanCleanup(unittest.TestCase):
    def test_simple(self):
        tmp = epub_cleaner.EpubCleaner('test/HenryVI.epub')
        tmp.setup()
        tmp.cleanup()
        self.assertFalse(os.path.exists('test/HenryVI'))
        self.assertFalse(os.path.exists('test/clean_HenryVI'))
        self.assertTrue(os.path.exists('test/clean_HenryVI.epub'))
if __name__ == '__main__':
    unittest.main()
