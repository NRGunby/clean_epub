import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os.path
root_xmlns = '{urn:oasis:names:tc:opendocument:xmlns:container}'
manifest_xmlns = '{http://www.idpf.org/2007/opf}'


def get_rightmost_string(element):
    tmp = element
    while not tmp.string:
        try:
            tmp = tmp.contents[-1]
        except IndexError:
            return ' ' # Is this robust? I don't think this is robust
    return tmp.string

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

def clean_html(html_txt, headers):
    soup = BeautifulSoup(html_txt)
    curr_para = None
    body = soup.body
    for each_body_element in body.contents:
        if each_body_element.name == 'p':
            each_body_string = get_rightmost_string(each_body_element).strip()
            if each_body_string.isdigit():
                each_body_element.decompose() #Bye-bye, scanned page number
            elif each_body_string in headers:
                each_body_element.decompose() # Bye-bye, headers
            elif each_body_string and each_body_string[-1] != '.':
                if curr_para:
                    while each_body_element.contents:
                        curr_para.append(each_body_element.contents[0])
                    each_body_element.decompose()
                else:
                    curr_para = each_body_element.extract()
            else:
                if curr_para:
                    while each_body_element.contents:
                        curr_para.append(each_body_element.contents[0])
                    each_body_element.replace_with(curr_para)
                    curr_para = None
    if curr_para:
        body.append(curr_para)
    return soup.prettify(formatter='html')
