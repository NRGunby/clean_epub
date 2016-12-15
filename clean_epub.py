from sys import argv
from epub_cleaner import EpubCleaner
if len(argv) == 1:
    print 'Usage: python clean_epub.py pathh/to/epub "Header Text 1" "Header Text 2"'
else:
    cleaner = EpubCleaner(argv[1])
    cleaner.process(argv[2:])
