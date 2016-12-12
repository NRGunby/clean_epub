import os.path

class EpubCleaner(object):
    def __init__(self, epub_name):
        self.old_epub_name = epub_name
        root_dir_name, epub_name = os.path.split(self.old_epub_name)
        old_base_name, ext_name = os.path.splitext(epub_name)
        new_base_name = 'clean_' + old_base_name
        self.old_dir_name = os.path.join(root_dir_name, old_base_name)
        self.new_dir_name = os.path.join(root_dir_name, new_base_name)
        self.new_epub_name = os.path.join(root_dir_name, new_base_name + ext_name)
