#!/usr/bin/env python3

import os
import sys
import argparse
import xml.etree.ElementTree as ET

class RadicalsProcessor:
    @staticmethod
    def _read_input(filepath):
        root = ET.parse(filepath).getroot()
        data = list()

        assert root.tag == 'radicals'

        for el in root:
            data.append({
                'symbol': el.find('symbol').text,
                'meaning': el.find('meaning').text,
                'pinyin': el.find('pinyin').text,
                'number': int(el.find('number').text),
                'strokes': int(el.find('strokes').text)
            })

        return data

    @staticmethod
    def _write_output(data, filepath):
        filename = os.path.splitext(os.path.basename(filepath))[0]

        with open(filepath, 'w') as file_obj:
            for el in data:
                file_obj.write('{}\t{}\t{}\t{}\t{}\n'.format(
                    el['symbol'],
                    el['pinyin'],
                    el['meaning'],
                    '{}_{:04}'.format(filename, el['number']),
                    filename
                ))

    @staticmethod
    def process(input, output):
        data = RadicalsProcessor._read_input(input)
        RadicalsProcessor._write_output(data, output)

class CharactersProcessor:
    @staticmethod
    def _read_input(filepath):
        root = ET.parse(filepath).getroot()
        data = list()

        assert root.tag == 'characters'

        for el in root:
            data.append({
                'symbol': el.find('symbol').text,
                'meaning': el.find('meaning').text,
                'pinyin': el.find('pinyin').text
            })

        return data

    @staticmethod
    def _write_output(data, filepath):
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

    @staticmethod
    def process(input, output):
        data = CharactersProcessor._read_input(input)
        CharactersProcessor._write_output(data, output)

class WordsProcessor:
    @staticmethod
    def _read_input(filepath):
        root = ET.parse(filepath).getroot()
        data = list()

        assert root.tag == 'words'

        for el in root:
            data.append({
                'chinese': el.find('chinese').text,
                'english': el.find('english').text,
                'pinyin': el.find('pinyin').text
            })

        return data

    @staticmethod
    def _write_output(data, filepath):
        filename = os.path.splitext(os.path.basename(filepath))[0]

        with open(filepath, 'w') as file_obj:
            count = 1
            for el in data:
                file_obj.write('{}\t{}\t{}\t{}\t{}\n'.format(
                    el['chinese'],
                    el['pinyin'],
                    el['english'],
                    '{}_{:04}'.format(filename, count),
                    filename
                ))
                count += 1

    @staticmethod
    def process(input, output):
        data = WordsProcessor._read_input(input)
        WordsProcessor._write_output(data, output)

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
    except IOError as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    main()
