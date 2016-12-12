import unittest
import epub_cleaner

class TestCleanSetup(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
