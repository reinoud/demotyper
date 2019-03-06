# Demotyper for Python


Do you give presentations where you switch from slides to a terminal screen to do an interactive demo?

Do these demo's sometimes fail? Do you suddenly make lots of typo's? Does this take you out of concentration?

### then this is the tool for you!

This is an improved version of hkrtpr, intended to 'demo' typing in a terminal window

Invoke with a source file to control what gets typed to the screen.

    demotyper.py /path/to/src/file

The screen wil clear, and the sourcefile will be displayed on the screen, with a few characters per keystroke. 
Just like you are typing them, but without any typo's!


Note: at the end of the file a capital Q is needed to exit, to make sure your screen is not suddenly empty again :-)

## advanced usage

### prompt

To start the session with a fake prompt, use the `-p` option like this

    demotyper.py -p '$ ' /path/to/src/file 
    
### skip whitespace

when you demo typing indented text -like sourcecode- it might look strange to have to type a lot of spaces, since modern 
editors will indent automatically. This behaviour can be be mimiced by `--skipwhitespace` or `-s`

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
  
use the `-a` option to accept any key (as opposed to `enter` before returning an output block)

## installation

copy the script in a directory in your path (/usr/bin on Linux or OSX) and make it executable (chmod +x demotyper.py)
