import xml.etree.ElementTree as ET
import os.path
epub_xmlns = '{urn:oasis:names:tc:opendocument:xmlns:container}'

def iter_rootfiles(epub_dir_name):
    container_tree = ET.parse(os.path.join(epub_dir_name, 'META-INF', 'container.xml'))
    try:
        for i in container_tree.getroot().find('rootfiles').findall('rootfile'):
            yield i.get('full-path')
    except AttributeError:
        for i in container_tree.getroot().find(epub_xmlns + 'rootfiles').findall(epub_xmlns + 'rootfile'):
            yield i.get('full-path')
