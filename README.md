# HackerTyper for Python

hkrtpr is intended to provide [HackerTyper][hackertyper]-style productivity for any machine with a
working python and curses implementation.

Invoke with a source file to control what gets typed to the screen.

  ./hackertyper.py /path/to/src/file.py


## advanced usage

when doing a demo, you can "type" commands, and get "output"

Put this in the file with special delimiters:

  - `<% t %>` start of a text block (will be treated normally)
  - `<% r %>` start of an output block (will appear at once when enter is pressed)
  
  example file:
  
  ```
  $ ls -a<% r %>
  .	..	.git .gitignore README.md hackertyper.py
  <% t %>
  $ file hackertyper.py<% r %>
  hackertyper.py: Python script text executable, ASCII text
  ```