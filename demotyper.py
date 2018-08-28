#!/usr/bin/python

import argparse
import curses
import random
import re
import sys

DELIMITERS = {'<% t %>': 'text',
              '<% r %>': 'return'}


class TextFile(object):
    def __init__(self, filename=None, prompt=''):
        self.raw_content = ''
        self.filtered_content = ''
        self.stops = {}
        self.prompt = prompt
        self.cursor_pos = len(self.prompt)
        if filename:
            self.readfile(filename)

    def readfile(self, filename):
        try:
            self.raw_content = self.prompt + open(filename).read()
        except Exception as e:
            sys.stderr.write("error reading file {}: {}".format(filename, e))
            sys.exit(1)
        self.filtered_content = self.filteredoutput(self.raw_content)
        self.findskippoints()

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
        try:
            nextstop = min([x for x in self.stops.keys() if x >= pos])
            delimiter_type = self.stops[nextstop]
        except ValueError:
            nextstop = len(self.filtered_content) + 1
            delimiter_type = 'end'
        return nextstop, delimiter_type

    @staticmethod
    def filteredoutput(string):
        """filter delimiters from string"""
        p = re.compile('(' + '|'.join(DELIMITERS.keys()) + ')')
        return p.sub('', string)

    def text(self, pos=None, maxlines=500):
        all_text = self.filtered_content[:pos]
        return '\n'.join(all_text.split('\n')[maxlines * -1:])

    def advance(self, key):
        """ advance the cursor in the document after a keystroke

        normal case: advance random 1-3 positions
        when a return delimiter is passed: stop at return position
        when at return position: key needs to be '\n' to advance to next text delimiter, otherwise stay
        """
        advance = random.choice(range(3))
        nextstop, delimiter_type = self.nextstop(self.cursor_pos)

        if delimiter_type == 'return' and nextstop == self.cursor_pos:
            if key == '\n':
                self.cursor_pos = self.nextstop(self.cursor_pos + 1)[0]
            # else wait; do not advance cursor
        elif delimiter_type == 'return' and self.cursor_pos + advance >= nextstop:
            self.cursor_pos = nextstop
        else:
            self.cursor_pos += advance


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", dest="filename", help="filename to demo")
    parser.add_argument("--prompt", "-p", dest="prompt", help="initial prompt", default='')
    local_args = parser.parse_args()
    if not local_args.filename:
        print "FATAL: need filename (see --help)"
        exit(1)
    return local_args


def main(stdscr):
    try:
        stdscr.clear()
        if len(args.prompt) > 0:
            contents = hackertyper.text(hackertyper.cursor_pos, stdscr.getmaxyx()[0])
            stdscr.addstr(0, 0, contents)
        while hackertyper.cursor_pos <= len(hackertyper.filtered_content):
            hackertyper.advance(stdscr.getkey())
            contents = hackertyper.text(hackertyper.cursor_pos, stdscr.getmaxyx()[0])
            stdscr.clrtoeol()
            stdscr.addstr(0, 0, contents)
        inputkey = ''
        while inputkey != 'Q':
            inputkey = stdscr.getkey()
    except KeyboardInterrupt:
        # clean exit without exception on screen when ctrl-C is pressed
        pass


if __name__ == '__main__':
    args = getargs()
    hackertyper = TextFile(args.filename, args.prompt)
    curses.wrapper(main)
