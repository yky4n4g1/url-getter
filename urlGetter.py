#!/usr/bin/env python3
import sys
import os.path
import argparse
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin


class HTMLAttrParser(HTMLParser):
    attrs = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            self.attrs.add((name, value))


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("url", help="url pls")
    argParser.add_argument("-f", "--filetype", type=str,
                           help="download file type")
    argParser.add_argument("-a", "--attribute", type=str,
                           help="インストールするファイルが指定されている属性")
    args = argParser.parse_args()

    if not args.url:
        print("Please specify URL.")
        sys.exit()
    if not (args.filetype or args.attribute):
        print("Please specefy attribute or filetype")
        sys.exit()
    elif args.filetype and args.filetype[0] != ".":
        args.filetype = "."+args.filetype

    with urllib.request.urlopen(args.url) as response:
        html = response.read()
    parser = HTMLAttrParser()
    parser.feed(html.decode('utf-8'))
    for attr, value in parser.attrs:
        value = urljoin(args.url, value)
        if args.attribute and args.filetype:
            if attr == args.attribute and os.path.splitext(value)[1] == args.filetype:
                print(value)
        elif args.attribute:
            if attr == args.attribute:
                print(value)
        elif args.filetype:
            if os.path.splitext(value)[1] == args.filetype:
                print(value)


if __name__ == "__main__":
    main()
