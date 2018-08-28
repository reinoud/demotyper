# Demotyper for Python

This is an improved version of hkrtpr, intended to 'demo' typing in a terminal window

Invoke with a source file to control what gets typed to the screen.

    demotyper.py -f /path/to/src/file

Note: at the end of the file a capital Q is needed to exit, to make sure your screen is not suddenly empty again :-)

## advanced usage

### prompt

To start the session with a fake prompt, use the `-p` option like this

    demotyper.py -f /path/to/src/file -p '$ '

### delimiters

when doing a demo, you can "type" commands, and get "output"

Put this in the file with special delimiters:

  - `<% t %>` start of a text block (will be treated normally)
  - `<% r %>` start of an output block (will appear at once when enter is pressed)
  
  example file:
  
  ```
  $ ls -a<% r %>
  .	..	.git .gitignore README.md demotyper.py
  <% t %>
  $ file demotyoer.py<% r %>
  demotyper.py: Python script text executable, ASCII text
  ```