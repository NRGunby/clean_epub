import unittest
import lib_epub
import epub_cleaner
from shutil import rmtree

class base(unittest.TestCase):
    def setUp(self):
        self.epub = epub_cleaner.EpubCleaner('test/HenryVI.epub')
        self.epub.setup()

    def tearDown(self):
        rmtree('test/HenryVI')
        rmtree('test/clean_HenryVI')

class TestIterRootfiles(base):
    def test_simple(self):
        ret = [i for i in lib_epub.iter_rootfiles(self.epub.new_dir_name)]
        self.assertEqual(ret, ['content.opf'])

if __name__ == '__main__':
    unittest.main()
