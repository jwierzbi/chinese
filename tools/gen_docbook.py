#!/usr/bin/env python3

import sys
import argparse
# import json
import xml.etree.ElementTree as ET
from functools import reduce
from collections import OrderedDict
from os.path import basename, splitext

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

def _process_radicals(args):
    root = ET.Element('article')
    root.set('xml:id', 'notes')
    root.set('xmlns', 'http://docbook.org/ns/docbook')
    root.set('version', '5.0')
    root.set('lang', 'en')

    sec = add_subelement(root, 'section')

    add_subelement(sec, 'title', args.input_file)

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

    for el in read_input(args.input_file)['radicals']:
        row = add_subelement(tbody, 'row')
        add_subelement(row, 'entry', el['number'])
        add_subelement(row, 'entry', el['symbol']) \
                .set('xml:id', 'r' + el['symbol'])
        add_subelement(row, 'entry', el['strokes'])
        add_subelement(row, 'entry', el['pinyin'])
        add_subelement(row, 'entry', el['meaning'])

    # ET.dump(root)
    tree = ET.ElementTree(root)
    tree.write(args.output_file, encoding='utf-8', xml_declaration=True)

def _process_characters(args):
    # if provided then load radicals first
    radicals = list()
    if args.radicals:
        radicals = [x['symbol'] for x in read_input(args.radicals)['radicals']]

    root = ET.Element('article')
    root.set('xml:id', 'notes')
    root.set('xmlns', 'http://docbook.org/ns/docbook')
    root.set('version', '5.0')
    root.set('lang', 'en')

    sec = add_subelement(root, 'section')

    add_subelement(sec, 'title', args.input_file)

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

    for el in read_input(args.input_file)['characters']:
        row = add_subelement(tbody, 'row')
        add_subelement(row, 'entry', el['symbol']) \
                .set('xml:id', 'ch' + el['symbol'])
        add_subelement(row, 'entry', el['pinyin'])

        if el['radical'] in radicals:
            r = add_subelement(row, 'entry')
            add_subelement(r, 'link', el['radical'],
                        linkend='r' + el['radical'])
        else:
            print('warning: no radical for character: {}'.format(el['symbol']))
            add_subelement(row, 'entry', el['symbol'])

        add_subelement(row, 'entry', ', '.join(el['components']) \
                if el['components'] else '')
        add_subelement(row, 'entry', el['meaning'])
        add_subelement(row, 'entry', el['note'] if 'note' in el else '')

    # ET.dump(root)
    tree = ET.ElementTree(root)
    tree.write(args.output_file, encoding='utf-8', xml_declaration=True)

def _process_words(args):
    # if provided then load characters first
    characters = list()
    if args.characters:
        for f in args.characters:
            characters += [
                x['symbol'] for x in read_input(f)['characters']
            ]

    # load all of the words
    words = OrderedDict()
    root = ET.parse(args.input_file).getroot()
    for word_el in root:
        word = OrderedDict()
        word['chinese'] = word_el.find('chinese').text
        word['pinyin'] = word_el.find('pinyin').text
        word['english'] = word_el.find('english').text

        if word['chinese'] in words:
            print('warning: word {} already exists, merging' \
                    .format(word['chinese']))

            old = words[word['chinese']]
            new = word

            t1 = [x.strip() for x in old['english'].split(';')]
            t2 = [x.strip() for x in new['english'].split(';')]

            for t in t2:
                if t not in t1:
                    t1.append(t)

            old['english'] = '; '.join(t1)
        else:
            words[word['chinese']] = word

    output_basename = splitext(basename(args.output_file))[0]

    if args.mode == 'anki':
        with open(args.output_file, 'w') as file_obj:
            count = 1
            for key in words:
                el = words[key]

                if len(el['chinese']) <= 1:
                    print('warning: word {} is only 1 character long' \
                            .format(el['chinese']))
                    continue

                # skip the word if we don't know all of the characters yet
                if not all(x in characters for x in el['chinese']):
                    print('warning: not all characters avaliable for word {}' \
                            .format(el['chinese']))
                    continue

                file_obj.write('{}\t{}\t{}\t{}\t{}\n'.format(
                    el['chinese'],
                    el['pinyin'],
                    el['english'],
                    '{}_{:04}'.format(output_basename, count),
                    output_basename
                ))
                count += 1
    elif args.mode == 'docbook':
        root = ET.Element('article')
        root.set('xml:id', 'notes')
        root.set('xmlns', 'http://docbook.org/ns/docbook')
        root.set('version', '5.0')
        root.set('lang', 'en')

        sec = add_subelement(root, 'section')

        add_subelement(sec, 'title', output_basename)

        table = add_subelement(sec, 'informaltable')
        tgroup = add_subelement(table, 'tgroup', cols='3')

        add_subelement(tgroup, 'colspec', colnum='1', colname='word-col1',
                       colwidth='1*')
        add_subelement(tgroup, 'colspec', colnum='2', colname='word-col2',
                       colwidth='2*')
        add_subelement(tgroup, 'colspec', colnum='3', colname='word-col3',
                       colwidth='4*')

        tbody = add_subelement(tgroup, 'tbody')

        for key in words:
            el = words[key]
            # skip the word if it's not at least 2 characters long
            if len(el['chinese']) <= 1:
                print('warning: word {} is only 1 character long' \
                        .format(el['chinese']))
                continue

            # skip the word if we don't know all of the characters yet
            if not all(x in characters for x in el['chinese']):
                print('warning: not all characters avaliable for word {}' \
                        .format(el['chinese']))
                continue

            row = add_subelement(tbody, 'row')

            word = add_subelement(row, 'entry')
            for ch in el['chinese']:
                add_subelement(word, 'link', ch, linkend='ch' + ch)

            add_subelement(row, 'entry', el['pinyin'])
            add_subelement(row, 'entry', el['english'])

        # ET.dump(root)
        tree = ET.ElementTree(root)
        tree.write(args.output_file, encoding='utf-8', xml_declaration=True)
    else:
        raise RuntimeError('wrong mode "{}"'.format(args.mode))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode', choices=('anki', 'docbook'),
                        required=True)

    subparsers = parser.add_subparsers()

    parser_radicals = subparsers.add_parser('radicals')
    parser_radicals.add_argument('-i', '--input_file', required=True)
    parser_radicals.add_argument('-o', '--output_file', required=True)
    parser_radicals.set_defaults(func=_process_radicals)

    parser_characters = subparsers.add_parser('characters')
    parser_characters.add_argument('-i', '--input_file', required=True)
    parser_characters.add_argument('-o', '--output_file', required=True)
    parser_characters.add_argument('-r', '--radicals')
    parser_characters.set_defaults(func=_process_characters)

    parser_words = subparsers.add_parser('words')
    parser_words.add_argument('-i', '--input_file', required=True)
    parser_words.add_argument('-o', '--output_file', required=True)
    parser_words.add_argument('-c', '--characters', nargs='+')
    parser_words.set_defaults(func=_process_words)

    args = parser.parse_args()

    try:
        args.func(args)
    except FileNotFoundError as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    main()
