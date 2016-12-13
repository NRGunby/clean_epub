import xml.etree.ElementTree as ET
import os.path
root_xmlns = '{urn:oasis:names:tc:opendocument:xmlns:container}'
manifest_xmlns = '{http://www.idpf.org/2007/opf}'

def iter_rootfiles(epub_dir_name):
    container_tree = ET.parse(os.path.join(epub_dir_name, 'META-INF', 'container.xml'))
    try:
        for i in container_tree.getroot().find('rootfiles').findall('rootfile'):
            yield os.path.join(epub_dir_name, i.get('full-path'))
    except AttributeError:
        for i in container_tree.getroot().find(root_xmlns + 'rootfiles').findall(root_xmlns + 'rootfile'):
            yield os.path.join(epub_dir_name, i.get('full-path'))

def iter_manifest(opf_filename):
    base_dirname = os.path.dirname(opf_filename)
    opf_tree = ET.parse(opf_filename)
    root = opf_tree.getroot()
    try:
        for i in root.find('manifest').findall('item'):
            href = i.get('href')
            if os.path.splitext(href)[1] in ('.html', '.xhtml'):
                yield os.path.join(base_dirname, href)
    except AttributeError:
        for i in root.find(manifest_xmlns + 'manifest').findall(manifest_xmlns + 'item'):
            href = i.get('href')
            if os.path.splitext(href)[1] in ('.html', '.xhtml'):
                yield os.path.join(base_dirname, href)
