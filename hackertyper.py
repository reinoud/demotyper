#!/usr/bin/python

import curses
import logging
import random
import re
import sys


DELIMITERS = {'<% t %>': 'text',
              '<% r %>': 'return'}


class TextFile(object):
    def __init__(self, filename=None):
        self.number_of_lines = 0
        self.raw_content = ''
        self.filtered_content = ''
        self.stops = {}
        self.filename = filename
        if filename:
            self.readfile(filename)

    def readfile(self, filename):
        try:
            self.raw_content = open(filename).read()
        except Exception as e:
            sys.stderr.write("error reading file {}: {}".format(filename, e))
            sys.exit(1)
        self.filtered_content = self.filteredoutput(self.raw_content)
        self.number_of_lines = self.lines_in_string(self.filtered_content)
        self.findskippoints()

    @staticmethod
    def lines_in_string(multilinestring):
        return len(multilinestring.splitlines())

    def findskippoints(self):
        """find points in the raw string that are marked by the delimiters

        This will return a dict with character position as key, and the type of delimiter as value:
        {36: 'text', 14: 'return'}

        Note that the positions are for removed delimiters, so they are correct for self.filtered_content
        """
        self.stops = {}
        regexp = re.compile('(' + '|'.join(DELIMITERS.keys()) + ')(.*)', re.DOTALL)  # match newline as well with '.'
        remaining = self.raw_content
        counter = 0
        while remaining:
            match = re.search(regexp, remaining)
            if match:
                counter += match.start()
                self.stops[counter] = DELIMITERS[match.group(1)]
                remaining = match.group(2)
            else:
                break

    def nextstop(self, pos):
        """return the next stop and the type of it after position pos in filtered_content """
        nextstop = min([x for x in self.stops.keys() if x >= pos])
        return nextstop, self.stops[nextstop]

    def lineforpos(self, pos):
        """ line number when cursor is at char pos in the file"""
        return self.lines_in_string(self.filtered_content[:pos])

    @staticmethod
    def filteredoutput(string):
        """filter delimiters from string"""
        p = re.compile('(' + '|'.join(DELIMITERS.keys()) + ')')
        return p.sub('', string)

    def text(self, pos):
        return self.filtered_content[:pos]


src = ""

logging.basicConfig(filename="hackertyper.log", level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def add_text(text_window, src_len):
    logging.debug("in add_text")
    # text_window.addstr(0,0,src[0:src_len])
    contents = hackertyper.text(src_len)
    # formatted_contents = highlight(contents, PythonLexer(), Terminal256Formatter())
    text_window.addstr(0, 0, contents)


def main(stdscr):
    """
    """
    logging.debug("starting hackertyper")
    logging.debug("read {} lines from file".format(hackertyper.number_of_lines, hackertyper.filename))
    stdscr.clear()
    logging.debug("clear")
    src_len = 0
    while True and src_len < len(hackertyper.filtered_content):
        logging.debug("top loop")
        add = random.choice(range(3))
        src_len += add
        inputkey = stdscr.getkey()
        logging.debug(inputkey)
        add_text(stdscr, src_len)


if __name__ == '__main__':
    logging.debug("----")
    filename_arg = sys.argv[-1]
    hackertyper = TextFile(filename_arg)
    curses.wrapper(main)
