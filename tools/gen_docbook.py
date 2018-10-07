#!/usr/bin/env python3

import sys
import argparse
# import json
import xml.etree.ElementTree as ET
from functools import reduce
from collections import OrderedDict

def is_list(element):
    return bool(reduce(lambda x,y: x if x == y else None,
                       [x.tag for x in element]))

# FIXME: ugly but works for now
def xml2dict(root, data=None):
    if data == None:
        data = list() if is_list(root) else OrderedDict()

    for child in root:
        if child: # has children
            if is_list(child):
                data[child.tag] = list()
                xml2dict(child, data[child.tag])
            else:
                if isinstance(data, list):
                    data.append(OrderedDict())
                    xml2dict(child, data[-1])
                else:
                    data[child.tag] = OrderedDict()
                    xml2dict(child, data[child.tag])
        else:
            if isinstance(data, list):
                data.append(child.text)
            else:
                data[child.tag] = child.text

    return data

def read_input(filepath):
    root = ET.parse(filepath).getroot()
    data = xml2dict(root)

    # json.dump(data, sys.stdout, indent=2)

    return {root.tag: data}

def add_subelement(root, tag, text=None, **kwargs):
    el = ET.SubElement(root, tag, kwargs)
    if text != None:
        el.text = text
    return el

class RadicalsProcessor:
    @staticmethod
    def process(input_file, output_file):
        root = ET.Element('article')
        root.set('xml:id', 'notes')
        root.set('xmlns', 'http://docbook.org/ns/docbook')
        root.set('version', '5.0')
        root.set('lang', 'en')

        sec = add_subelement(root, 'section')

        add_subelement(sec, 'title', input_file)

        table = add_subelement(sec, 'informaltable')
        tgroup = add_subelement(table, 'tgroup', cols='5')

        add_subelement(tgroup, 'colspec', colnum='1', colname='rad-col1',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='2', colname='rad-col2',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='rad-col3',
                       colwidth='1.2*')
        add_subelement(tgroup, 'colspec', colnum='4', colname='rad-col4',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='5', colname='rad-col5',
                       colwidth='3*')

        tbody = add_subelement(tgroup, 'tbody')

        for el in read_input(input_file)['radicals']:
            row = add_subelement(tbody, 'row')
            add_subelement(row, 'entry', el['number'])
            add_subelement(row, 'entry', el['symbol'])
            add_subelement(row, 'entry', el['strokes'])
            add_subelement(row, 'entry', el['pinyin'])
            add_subelement(row, 'entry', el['meaning'])

        # ET.dump(root)
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

class CharactersProcessor:
    @staticmethod
    def process(input_file, output_file):
        root = ET.Element('article')
        root.set('xml:id', 'notes')
        root.set('xmlns', 'http://docbook.org/ns/docbook')
        root.set('version', '5.0')
        root.set('lang', 'en')

        sec = add_subelement(root, 'section')

        add_subelement(sec, 'title', input_file)

        table = add_subelement(sec, 'informaltable')
        tgroup = add_subelement(table, 'tgroup', cols='6')

        add_subelement(tgroup, 'colspec', colnum='1', colname='char-col1',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='2', colname='char-col2',
                       colwidth='1.2*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='char-col3',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='4', colname='char-col4',
                       colwidth='1.2*')
        add_subelement(tgroup, 'colspec', colnum='5', colname='char-col5',
                       colwidth='2*')
        add_subelement(tgroup, 'colspec', colnum='6', colname='char-col6',
                       colwidth='3*')

        tbody = add_subelement(tgroup, 'tbody')

        for el in read_input(input_file)['characters']:
            row = add_subelement(tbody, 'row')
            add_subelement(row, 'entry', el['symbol'])
            add_subelement(row, 'entry', el['pinyin'])
            add_subelement(row, 'entry', el['radical'])
            add_subelement(row, 'entry', ', '.join(el['components']) \
                    if el['components'] else '')
            add_subelement(row, 'entry', el['meaning'])
            add_subelement(row, 'entry', el['note'] if 'note' in el else '')

        # ET.dump(root)
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

class WordsProcessor:
    @staticmethod
    def process(input_file, output_file):
        root = ET.Element('article')
        root.set('xml:id', 'notes')
        root.set('xmlns', 'http://docbook.org/ns/docbook')
        root.set('version', '5.0')
        root.set('lang', 'en')

        sec = add_subelement(root, 'section')

        add_subelement(sec, 'title', input_file)

        table = add_subelement(sec, 'informaltable')
        tgroup = add_subelement(table, 'tgroup', cols='3')

        add_subelement(tgroup, 'colspec', colnum='1', colname='word-col1',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='2', colname='word-col2',
                       colwidth='2*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='word-col3',
                       colwidth='4*')

        tbody = add_subelement(tgroup, 'tbody')

        for el in read_input(input_file)['words']:
            row = add_subelement(tbody, 'row')
            add_subelement(row, 'entry', el['chinese'])
            add_subelement(row, 'entry', el['pinyin'])
            add_subelement(row, 'entry', el['english'])

        # ET.dump(root)
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    parser.add_argument('-t', '--type', required=True,
                        choices=('radicals', 'chars', 'words'))
    args = parser.parse_args()

    processors = {
        'radicals': RadicalsProcessor,
        'chars': CharactersProcessor,
        'words': WordsProcessor
    }

    try:
        processors[args.type].process(args.input_file, args.output_file)
    except FileNotFoundError as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    main()
