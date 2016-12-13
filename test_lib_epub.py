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
        self.assertEqual(ret, [self.epub.new_dir_name + '/content.opf'])

class TestIterManifest(base):
    def test_simple(self):
        tmp = [i for i in lib_epub.iter_rootfiles(self.epub.new_dir_name)]
        ret = [i for i in lib_epub.iter_manifest(tmp[0])]
        self.assertEqual(ret[0], self.epub.new_dir_name + '/index_split_000.html')
        self.assertEqual(len(ret), 68)

if __name__ == '__main__':
    unittest.main()
