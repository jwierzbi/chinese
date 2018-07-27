#!/usr/bin/python3

import sys
import argparse
import xml.etree.ElementTree as ET

def read_input(filepath):
    root = ET.parse(filepath).getroot()
    data = list()

    for child in root:
        assert child.tag == 'character'

        ch = dict()

        tags = ('symbol', 'pinyin', 'meaning')

        for tag in tags:
            el = child.find(tag)
            ch[tag] = el.text

        data.append(ch)

    return data

def write_output(data, filepath):
    root = ET.Element('article')
    root.set('xml:id', 'characters')
    root.set('xmlns', 'http://docbook.org/ns/docbook')
    root.set('version', '5.0')
    root.set('lang', 'en')

    section = ET.SubElement(root, 'section')
    title = ET.SubElement(section, 'title')
    title.text = filepath # FIXME: this should be a sensible title

    for el in data:
        subsection = ET.SubElement(section, 'section')

        title = ET.SubElement(subsection, 'title')
        title.text = el['symbol']

        pinyin = ET.SubElement(subsection, 'para')
        pinyin.text = 'pinyin: ' + el['pinyin']

        meaning = ET.SubElement(subsection, 'para')
        meaning.text = 'meaning: ' + el['meaning']

    #ET.dump(root)
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()

    try:
        data = read_input(args.input_file)
    except FileNotFoundError as ex:
        print(ex)
        sys.exit(1)

    write_output(data, args.output_file)

if __name__ == '__main__':
    main()
