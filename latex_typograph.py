''' LaTeX Typograph
    Version 2.0 (2021-03-24)
    Copyright (c) 2021 Evgenii Shirokov
    MIT License
'''

import os
import regex  # https://pypi.org/project/regex/


def typograph(text: str):
    '''This function replaces the space and/or tab characters
    with the non-breaking spaces ~ in LaTeX documents
    before the spaced en/em dashes and reference commands.
    It returns the improved LaTeX code (str)
    and the number of substitutions made (int).
    It can mess things up so be careful when using it.
    '''
    s = r'[ \t]+'  # one or more consecutive space and tab characters

    # Handle dashes (ignore file or newline beginning):
    find_1 = r'(?<!(?:\n|^)[ \t]*)' + s + '(--|–|---|—)' + s
    text, count = regex.subn(find_1, r'~\1 ', text, regex.VERSION0)

    # References (command, its shortenings, and symbols after command):
    refs = {'ref':     ('Refs?|Eqs?|Figs?', r'\{'),    # after \ref:      {
            'pageref': ('pp?',              r'\{'),    # after \pageref:  {
            'eqref':   ('Eqs?',             r'\{'),    # after \eqref:    {
            'cite':    ('Refs?',            r'\{|\[')  # after \cite:     { [
            }
    # Symbols before a whitespace character and a reference command:
    pre_ref = (r"(?<!\\[a-zA-Z]*)[a-zA-Z]|"  # Latin letter (but not \command)
               r"[0-9]|"                     # digit
               r"(?<!\.|\?|\!)(?:''|”)|"     # '' ” not preceded by .?!
               r"(?<!\.|\?|\!|')(?:'|’)|"    # ' ’  not preceded by .?!'
               r"\\%|"                       # \%   but not comment %
               r"\$|"                        # $    USD and end of $...$
               r"(?<!\.|\?|\!)(?:\)|\])|"    # ) ]  not preceded by .?!
               r"\}"                         # }    i.e., \}, {...}
               )
    # Symbols immediately before a reference shorthand:
    pre_short = (r" |\t|^|\n|"  # space, \t; file or newline beginning
                 r"\[|\(|"      # [ (
                 r"\{|"         # {      i.e., \{ and in {...}, \xx{...}
                 r"`|‘|“"       # opening quotes: ` `` “ ‘
                 )
    # Handle references:
    for key, val in refs.items():
        cmd = r'\\' + key + '(?:' + val[1] + ')'
        find_2 = '(' + pre_ref + ')' + s + '(' + cmd + ')'
        text, num = regex.subn(find_2, r'\1~\2', text, regex.VERSION0)
        count += num
        find_3 = '(' + pre_short + ')(' + val[0] + r')\.' + s + '(' + cmd + ')'
        text, num = regex.subn(find_3, r'\1\2.~\3', text, regex.VERSION0)
        count += num

    return text, count  # return the improved code and number of substitutions


if __name__ == '__main__':

    # Path and encoding of your LaTeX file:
    path = r'document.tex'
    enc = 'utf8'

    # Read LaTeX file:
    with open(path, mode='r', encoding=enc) as f:
        text = f.read()
    print(f'input:\t{path}')

    # Call typograph():
    new_text, count = typograph(text)

    # Generate a new unique filename in the same directory:
    root, ext = os.path.splitext(path)
    def get_path(): return f'{root}.{str(i).zfill(2)}{ext}' if i > 0 else path
    i = 0
    while os.path.exists(get_path()): i += 1
    new_path = get_path()

    # Save the improved LaTeX code to the new file:
    with open(new_path, mode='w', encoding=enc) as f:
        f.write(new_text)
    print(f'output:\t{new_path}')
    print(f'number of substitutions: {count}')
