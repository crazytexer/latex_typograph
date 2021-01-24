''' LaTeX Typograph
    Version 1.0 (25 January 2021)
    Copyright (c) 2021 Evgenii Shirokov
    MIT License
'''

import os
import string
import regex  # https://pypi.org/project/regex/


def typograph(text: str):
    '''This function replaces the space characters
    with the non-breaking spaces ~ in LaTeX documents
    before the spaced en/em dashes and reference commands.
    It returns the improved LaTeX code (str)
    and the found non-ASCII characters (list).
    It can mess things up so be careful when using it.
    '''

    # Consecutive space characters (space, \t):
    s = r'[ \t]+'

    # Replace the space characters with the non-breaking space (NBSP)
    # before the spaced en/em dash unless it starts a new line or a file:
    for dash in ['--', '---']:
        old = r'(?<!(?:^|\n)[ \t]*)' + s + dash + s
        new = '~' + dash + ' '
        text = regex.sub(old, new, text, regex.VERSION0)

    # Reference commands:
    ref = 'cite|eqref|ref|pageref'

    # Replace the space characters with NBSP
    # between the following characters and a reference:
    pre_ref = (r"(?<!\\[a-zA-Z]*)[a-zA-Z]|"  # letter (unless \command)
               r"[0-9]|"                     # digit
               r"(?<!\.|\?|\!)(?:'')|"       # ''   not preceded by .?!
               r"(?<!\.|\?|\!|')(?:')|"      # '    not preceded by .?!'
               r"\\%|"                       # \%   but not comment %
               r"\$|"                        # $    USD and end of $..$
               r"(?<!\.|\?|\!)(?:\)|\])|"    # ) ]  not preceded by .?!
               r"\}"                         # }    i.e., \}, {...}
               )
    old = '(' + pre_ref + ')' + s + r'\\(' + ref + r')\{'
    new = r'\1~\\\2{'
    text = regex.sub(old, new, text, regex.VERSION0)

    # Shortenings of reference names
    # (Fig., Figs., Ref., Refs., Eq., Eqs., Sec., P., p.):
    short = 'Figs?|Refs?|Eqs?|Sec|P|p'

    # Replace the space characters with NBSP
    # between the following characters+shortening+dot and a reference:
    pre_short = (r"^|\n|"   # 1st characters in a file, newline
                 r" |\t|"   # space, \t
                 r"\[|\(|"  # [ (
                 r"\{|"     # {      i.e., \{ and in {...}, \xx{...}
                 r"`"       # opening quotes: ` or ``
                 )
    old = '(' + pre_short + ')(' + short + r')\.' + s + r'\\(' + ref + r')\{'
    new = r'\1\2.~\\\3{'
    text = regex.sub(old, new, text, regex.VERSION0)

    # ASCII characters that are considered to be acceptable in LaTeX documents
    # (formfeed and vertical tab from string.whitespace are not included):
    ASCII_chars = string.ascii_letters + string.digits + string.punctuation \
                  + ' \t\r\n'

    # Search for non-ASCII characters:
    non_ASCII_chars = []
    for s in text:
        if s not in ASCII_chars:
            non_ASCII_chars.append(s)

    # Return the improved LaTeX code and the non-ASCII characters:
    return text, non_ASCII_chars


if __name__ == '__main__':

    # Your LaTeX file:
    file = r'document.tex'

    # Its encoding:
    enc = 'utf8'

    print(f'file {file}')

    # Read the LaTeX file:
    with open(file, mode='r', encoding=enc) as f:
        text = f.read()

    # Call the typograph() function:
    new_text, non_ASCII_chars = typograph(text)

    # Generate the new filename in the same directory:
    root, ext = os.path.splitext(file)

    def filename(i):
        return f'{root}.{str(i).zfill(2)}{ext}'

    i = 1
    while os.path.exists(filename(i)):
        i += 1
    new_file = filename(i)

    # Save the improved LaTeX code to the new file:
    with open(new_file, mode='w', encoding=enc) as f:
        f.write(new_text)
    print(f'saved to {new_file}')

    # Print the non-ASCII characters from your file and their Unicode codes:
    if non_ASCII_chars:
        print('non-ASCII characters and their codes:')
        for ch in non_ASCII_chars:
            unicode = 'U+' + format(ord(ch), 'x').upper().zfill(4)
            print(f'{ch} {unicode}')
