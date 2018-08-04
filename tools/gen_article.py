#!/usr/bin/env python3

import sys
import argparse
import xml.etree.ElementTree as ET

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()

    ET.register_namespace('', 'http://docbook.org/ns/docbook')

    root = ET.Element('article')
    root.set('xml:id', 'characters')
    root.set('version', '5.0')
    root.set('lang', 'en')

    for filename in args.files:
        local_root = ET.parse(filename).getroot()
        assert local_root.tag == '{http://docbook.org/ns/docbook}article'

        for section in local_root:
            root.append(section)

    ET.ElementTree(root).write(args.output_file, encoding='utf-8',
                               xml_declaration=True)

if __name__ == '__main__':
    main()
