import os.path
import lib_epub
import zipfile
from shutil import copytree, rmtree
from os import mkdir, walk


class EpubCleaner(object):
    def __init__(self, epub_name):
        self.old_epub_name = epub_name
        root_dir_name, epub_name = os.path.split(self.old_epub_name)
        old_base_name, ext_name = os.path.splitext(epub_name)
        new_base_name = 'clean_' + old_base_name
        self.old_dir_name = os.path.join(root_dir_name, old_base_name)
        self.new_dir_name = os.path.join(root_dir_name, new_base_name)
        self.new_epub_name = os.path.join(root_dir_name, new_base_name + ext_name)

    def setup(self):
        old_epub_zip = zipfile.ZipFile(self.old_epub_name)
        mkdir(self.old_dir_name)
        old_epub_zip.extractall(self.old_dir_name)
        copytree(self.old_dir_name, self.new_dir_name)

    def cleanup(self):
        new_epub_zip = zipfile.ZipFile(self.new_epub_name, 'w')
        for root, dirs, files in walk(self.new_dir_name):
            for fname in files:
                new_epub_zip.write(os.path.join(root, fname))
        new_epub_zip.close()
        rmtree(self.old_dir_name)
        rmtree(self.new_dir_name)

    def process(self, headers):
        self.setup()
        for each_rootfile in lib_epub.iter_rootfiles(self.new_dir_name):
            for each_html_file in lib_epub.iter_manifest(each_rootfile):
                with open(each_html_file) as f:
                    each_html_txt = f.read()
                new_html_txt = lib_epub.clean_html(each_html_txt, headers)
                with open(each_html_file, 'w') as f:
                    f.write(new_html_txt)
        self.cleanup()
