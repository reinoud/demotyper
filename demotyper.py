#!/usr/bin/python

import argparse
import curses
import random
import re
import sys

DELIMITERS = {'<% t %>': 'text',
              '<% r %>': 'return'}


class TextFile(object):
    def __init__(self, filename=None, prompt='', anykey=False, skipwhitespace=False):
        self.raw_content = ''
        self.filtered_content = ''
        self.stops = {}
        self.prompt = prompt
        self.anykey = anykey
        self.skipwhitespace = skipwhitespace
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
        {36: 'text', 14: 'return'} (stored in self.stops)

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

    def text(self, pos=None, maxyx=(500, 80)):
        """return the contents until pos, cut off everything outside of the window boundaries"""
        all_text = self.filtered_content[:pos]
        lines = all_text.split('\n')[(maxyx[0] - 1) * -1:]
        for lineno, line in enumerate(lines):
            lines[lineno] = line[:maxyx[1] - 1]
        return '\n'.join(lines)

    def advance(self, key):
        """ advance the cursor in the document after a keystroke

        normal case: advance random 1-3 positions
        when a return delimiter is passed: stop at return position
        when at return position: key needs to be '\n' to advance to next text delimiter, otherwise stay
        """
        advance = random.choice(range(3))
        nextstop, delimiter_type = self.nextstop(self.cursor_pos)

        if delimiter_type == 'return' and nextstop == self.cursor_pos:
            if key == '\n' or self.anykey:
                self.cursor_pos = self.nextstop(self.cursor_pos + 1)[0]
            # else wait; do not advance cursor
        elif delimiter_type == 'return' and self.cursor_pos + advance >= nextstop:
            self.cursor_pos = nextstop
        else:
            self.cursor_pos += advance
            if self.skipwhitespace:
                try:
                    while self.filtered_content[self.cursor_pos] == ' ':
                        self.cursor_pos += 1
                except IndexError:
                    self.cursor_pos -= 1


def getargs():
    parser = argparse.ArgumentParser(description='Simulate typing and output in a terminal window. ' +
                                    'Use <% r %> to wait for return and output everything until <% t %>')
    parser.add_argument("--prompt", "-p", dest="prompt", help="initial prompt", default='')
    parser.add_argument("--anykey", "-a", dest="anykey",
                        help="accept any key before returning output block (instead of only enter)",
                        action="store_true", default=False)
    parser.add_argument("--skipwhitespace", "-s", dest="skipwhitespace", help="skip whitespace while typing",
                        action="store_true", default=False)
    parser.add_argument("filename", help="filename to simulate typing")
    return parser.parse_args()


def main(stdscr):
    try:
        stdscr.clear()
        if len(args.prompt) > 0:
            contents = demotyper.text(demotyper.cursor_pos, stdscr.getmaxyx())
            stdscr.addstr(0, 0, contents)
        while demotyper.cursor_pos <= len(demotyper.filtered_content):
            demotyper.advance(stdscr.getkey())
            contents = demotyper.text(demotyper.cursor_pos, stdscr.getmaxyx())
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
    demotyper = TextFile(args.filename, args.prompt, args.anykey, args.skipwhitespace)
    curses.wrapper(main)
