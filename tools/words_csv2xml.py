#!/usr/bin/env python3

import argparse
import csv
import xml.etree.ElementTree as ET
from collections import OrderedDict

def csv2xml(csv_filename, xml_filename):
    words = list()

    with open(csv_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            word = OrderedDict()
            word['chinese'] = row[1]
            word['pinyin'] = row[2]
            word['english'] = row[3]

            if row[0]:
                word['comment'] = row[0]

            words.append(word)

    root = ET.Element('words')

    for word in words:
        if 'comment' in word:
            comment = ET.Comment(word['comment'])
            root.append(comment)

        word_el = ET.SubElement(root, 'word')

        el = ET.SubElement(word_el, 'chinese')
        el.text = word['chinese']
        el = ET.SubElement(word_el, 'pinyin')
        el.text = word['pinyin']
        el = ET.SubElement(word_el, 'english')
        el.text = word['english']

    if xml_filename == '-':
        print('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>')
        print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
    else:
        ET.ElementTree(root).write(xml_filename, encoding='utf-8',
                                   xml_declaration=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv', required=True)
    parser.add_argument('-x', '--xml', required=True)
    args = parser.parse_args()

    csv2xml(args.csv, args.xml)

if __name__ == '__main__':
    main()