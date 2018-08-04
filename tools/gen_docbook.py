#!/usr/bin/env python3

import sys
import argparse
import xml.etree.ElementTree as ET

def read_input(filepath):
    root = ET.parse(filepath).getroot()
    data = list()

    if root.tag == 'characters':
        tags = ('symbol', 'pinyin', 'meaning', 'note', 'radical')
    elif root.tag == 'radicals':
        tags = ('number', 'symbol', 'pinyin', 'meaning', 'strokes')
    else:
        raise RuntimeError('invalid file format')

    for child in root:
        assert child.tag == 'character' or child.tag == 'radical'

        ch = dict()

        for tag in tags:
            el = child.find(tag)
            if el != None and el.text:
                ch[tag] = el.text

        data.append(ch)

    return {'type': root.tag, 'data': data}

def add_subelement(root, tag, text=None, **kwargs):
    el = ET.SubElement(root, tag, kwargs)
    if text != None:
        el.text = text

def write_output(data, filepath):
    root = ET.Element('article')
    root.set('xml:id', 'characters')
    root.set('xmlns', 'http://docbook.org/ns/docbook')
    root.set('version', '5.0')
    root.set('lang', 'en')

    sec = ET.SubElement(root, 'section')
    title = ET.SubElement(sec, 'title')
    title.text = filepath # FIXME: this should be a sensible title

    for el in data['data']:
        subsec = ET.SubElement(sec, 'section')

        if data['type'] == 'characters':
            add_subelement(subsec, 'title', el['symbol'])
            add_subelement(subsec, 'para', 'pinyin: ' + el['pinyin'])
            # FIXME: the feild should be mandatory
            if 'radical' in el:
                add_subelement(subsec, 'para', 'radical: ' + el['radical'])
            add_subelement(subsec, 'para', 'meaning: ' + el['meaning'])
            # FIXME: the feild should be mandatory
            if 'note' in el:
                add_subelement(subsec, 'para', 'note: ' + el['note'])
        elif data['type'] == 'radicals':
            add_subelement(subsec, 'title',
                           '{} {}'.format(el['number'], el['symbol']))
            add_subelement(subsec, 'para', 'strokes: ' + el['strokes'])
            add_subelement(subsec, 'para', 'pinyin: ' + el['pinyin'])
            add_subelement(subsec, 'para', 'meaning: ' + el['meaning'])

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
