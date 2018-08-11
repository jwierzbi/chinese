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

def write_output(data, filepath):
    root = ET.Element('article')
    root.set('xml:id', 'characters')
    root.set('xmlns', 'http://docbook.org/ns/docbook')
    root.set('version', '5.0')
    root.set('lang', 'en')

    sec = ET.SubElement(root, 'section')
    # FIXME: this should be a sensible title
    add_subelement(sec, 'title', filepath)

    table = add_subelement(sec, 'informaltable')

    if 'characters' in data:
        tgroup = add_subelement(table, 'tgroup', cols='6')

        add_subelement(tgroup, 'colspec', colnum='1', colname='col1',
                    colwidht='1*')
        add_subelement(tgroup, 'colspec', colnum='2', colname='col2',
                    colwidht='1.2*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='col3',
                    colwidht='1*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='col3',
                    colwidht='1.2*')
        add_subelement(tgroup, 'colspec', colnum='4', colname='col4',
                    colwidht='2*')
        add_subelement(tgroup, 'colspec', colnum='5', colname='col5',
                    colwidht='3*')

        tbody = add_subelement(tgroup, 'tbody')

        for el in data['characters']:
            row = add_subelement(tbody, 'row')
            add_subelement(row, 'entry', el['symbol'])
            add_subelement(row, 'entry', el['pinyin'])
            add_subelement(row, 'entry', el['radical'])
            add_subelement(row, 'entry', ', '.join(el['components']) \
                    if el['components'] else '')
            add_subelement(row, 'entry', el['meaning'])
            add_subelement(row, 'entry', el['note'] if 'note' in el else '')
    elif 'radicals' in data:
        tgroup = add_subelement(table, 'tgroup', cols='4')

        add_subelement(tgroup, 'colspec', colnum='1', colname='col1',
                    colwidht='1*')
        add_subelement(tgroup, 'colspec', colnum='2', colname='col2',
                    colwidht='1.2*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='col3',
                    colwidht='1*')
        add_subelement(tgroup, 'colspec', colnum='4', colname='col4',
                    colwidht='3*')

        tbody = add_subelement(tgroup, 'tbody')

        for el in data['radicals']:
            row = add_subelement(tbody, 'row')
            add_subelement(row, 'entry',
                            '{} {}'.format(el['number'], el['symbol']))
            add_subelement(row, 'entry', el['strokes'])
            add_subelement(row, 'entry', el['pinyin'])
            add_subelement(row, 'entry', el['meaning'])

    # ET.dump(root)
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
