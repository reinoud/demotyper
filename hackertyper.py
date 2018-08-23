#!/usr/bin/python

import sys
import curses

import logging
import random


src = ""

logging.basicConfig(filename="hackertyper.log", level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def add_text(text_window, src_len):
    
    logging.debug("add_text entered")
    # text_window.addstr(0,0,src[0:src_len])
    contents = src[0:src_len]
    # formatted_contents = highlight(contents, PythonLexer(), Terminal256Formatter())
    text_window.addstr(0, 0, contents)
    

def main(stdscr):
    """
    """
    logging.debug("starting hackertyper")    
    stdscr.clear()
    src_len = 0
    while True and src_len < len(src):
        add = random.choice(range(3))
        src_len += add
        inputkey = stdscr.getkey()
        logging.debug(inputkey)
        add_text(stdscr, src_len)
      

if __name__ == '__main__':
    # load the file that should be used for the hackertyper
    src = open(sys.argv[-1]).read()
    curses.wrapper(main)    

