#!/usr/bin/env python3

import os
import sys
import argparse
import xml.etree.ElementTree as ET

def read_input(filepath):
    root = ET.parse(filepath).getroot()
    data = list()

    if root.tag != 'characters':
        # ignore radicals
        return dict()

    for el in root:
        data.append({
            'symbol': el.find('symbol').text,
            'meaning': el.find('meaning').text,
            'pinyin': el.find('pinyin').text
        })

    return data

def write_output(data, filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, 'w') as file_obj:
        count = 1
        for el in data:
            file_obj.write('{}\t{}\t{}\t{}\t{}\n'.format(
                el['symbol'],
                el['pinyin'],
                el['meaning'],
                '{}_{:04}'.format(filename, count),
                filename
            ))
            count += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()

    try:
        data = read_input(args.input_file)
    except IOError as ex:
        print(ex)
        sys.exit(1)

    write_output(data, args.output_file)

if __name__ == '__main__':
    main()
