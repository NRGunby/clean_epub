import lib_epub
import epub_cleaner
import unittest
from shutil import rmtree
from bs4 import BeautifulSoup

class base(unittest.TestCase):
    def setUp(self):
        self.epub = epub_cleaner.EpubCleaner('test/HenryVI.epub')
        self.epub.setup()

    def tearDown(self):
        rmtree('test/clean_HenryVI')

class TestIterRootfiles(base):
    def test_simple(self):
        ret = [i for i in lib_epub.iter_rootfiles(self.epub.dir_name)]
        self.assertEqual(ret, [self.epub.dir_name + '/content.opf'])

class TestIterManifest(base):
    def test_simple(self):
        tmp = [i for i in lib_epub.iter_rootfiles(self.epub.dir_name)]
        ret = [i for i in lib_epub.iter_manifest(tmp[0])]
        self.assertEqual(ret[0], self.epub.dir_name + '/index_split_000.html')
        self.assertEqual(len(ret), 68)

class TestCleanHTML(unittest.TestCase):
    def begin(self, name):
        before_txt = open(name).read()
        after_txt = lib_epub.clean_html(before_txt, ['This is a header'])
        after_soup = BeautifulSoup(after_txt)
        # Standardise formating before and after
        before_soup = BeautifulSoup(BeautifulSoup(before_txt).prettify())
        return before_soup, after_soup

    def test_accumulate(self):
        before_soup, after_soup = self.begin('test/accumulate.html')
        self.assertEqual(before_soup.head, after_soup.head)
        after_p = after_soup.find_all('p')
        self.assertEqual(len(after_p), 2)
        self.assertEqual(len(after_p[0].string.split()), 40)

    def test_preserve(self):
        before_soup, after_soup = self.begin('test/preserve.html')
        self.assertEqual(before_soup.head, after_soup.head)
        self.assertEqual(before_soup.body, after_soup.body)

    def test_hanging(self):
        before_soup, after_soup = self.begin('test/hanging.html')
        self.assertEqual(before_soup.head, after_soup.head)
        after_p = after_soup.find_all('p')
        self.assertEqual(len(after_p), 2)

    def test_remove(self):
        before_soup, after_soup = self.begin('test/remove.html')
        self.assertEqual(before_soup.head, after_soup.head)
        after_p = after_soup.find_all('p')
        self.assertEqual(len(after_p), 2)

    def test_nested(self):
        before_soup, after_soup = self.begin('test/nested_tags.html')
        self.assertTrue(after_soup.i)

if __name__ == '__main__':
    unittest.main()
