# LaTeX Typograph

In LaTeX documents, the Python script `latex_typograph.py` replaces the spaces and/or TABs with non-breaking spaces&nbsp;`~` before the spaced en and em dashes (`--` and `---`) and reference commands (`\cite`, `\eqref`, `\ref`, and `\pageref`) using regular expressions. The `typograph(text: str)` function&mdash;the core part of this script&mdash;returns the improved LaTeX code&nbsp;(`str`) and the found non-ASCII characters&nbsp;(`list`). The script can mess up your document so be careful when using it (see details below).

## What It Can Do: Examples

| Input                                          | Output                                              |
|:-----------------------------------------------|:----------------------------------------------------|
| `Some scripts -- such this one -- are nice.`   | `Some scripts~-- such this one~-- are nice.`        |
| `Some scripts --- such this one --- are nice.` | `Some scripts~--- such this one~--- are nice.`      |
| `Some scripts---such this one---are nice.`     | (no changes because the dashes are not spaced)      |
| `as it is shown in \cite{wang2020}`            | `as it is shown in~\cite{wang2020}`                 |
| `see Equation \eqref{sq}`                      | `see Equation~\eqref{sq}`                           |
| `listing \ref{lst}`                            | `listing~\ref{lst}`                                 |
| `on page \pageref{lst}`                        | `on page~\pageref{lst}`                             |
| `never before. \cite{wang2020} shows` | (generally no changes between `.,:;?!` and a&nbsp;reference) |
| `in Fig. \ref{fig}`                   | `in Fig.~\ref{fig}` (but `Fig.` allows `~`)                  |
| `in {\bf \ref{fig}}`                  | (no changes between any `\command` and a&nbsp;reference)     |

## Details

1. It is supposed that your LaTeX document is initially prepared correctly. The `typograph(text: str)` function&mdash;the core part of this script&mdash;does not correct any typesetting mistakes. It just replaces spaces and/or TABs with the non-breaking space (NBSP)&nbsp;`~` where necessary.

2. Since LaTeX considers multiple consecutive whitespace characters as a&nbsp;single space character, this script works correctly if it finds multiple consecutive spaces and/or TABs around dashes and before reference commands.

3. The space characters are replaced with the NBSP before the spaced en/em dash (`--` and&nbsp;`---`) unless it starts a&nbsp;new line (because the leading whitespace characters in the line are ignored by&nbsp;LaTeX).

4. The NBSP is inserted instead of the space characters between **(a)**&nbsp;a&nbsp;Latin letter (`a`...`z`, `A`...`Z`), a&nbsp;digit (`0`...`9`), the&nbsp;closing quote `'` (and `''`), the percent sign in LaTeX&nbsp;`\%` (but not the comment `%`), the dollar sign&nbsp;`$` (which means both USD&nbsp;`\$` and the end of inline equation&nbsp;`$...$`), a&nbsp;closing bracket (`)`, `]`, and&nbsp;`}`; the latter means both the bracket itself&nbsp;`\}` and the end of&nbsp;`\command{...}`) and **(b)**&nbsp;a&nbsp;reference command (`\cite{...}`, `\eqref{...}`, `\ref{...}`, and `\pageref{...}`).

5. Note that this script is supposed to be used if citations appear as&nbsp;[1]. If it is something like [Wang, 2020], then the NBSP before it may be unnecessary but the script does not care about it. In such cases, you may want to remove `cite|` from line&nbsp;32 (`ref = 'cite|eqref|ref|pageref'`).

6. Generally no changes are made if a&nbsp;reference command is preceded by **(a)**&nbsp;a&nbsp;punctuation mark (`.,:;?!`) and **(b)**&nbsp;the space characters because the mark and the reference belong to logically different segments. The same goes for a&nbsp;preceding sentence in brackets or quotation marks (i.e., which ends with `.)`, `?)`, `!)`, `.]`, `?]`, `!]`, `.'`, `?'`, `!'`, `.''`, `?''`, or `!''`).

7. The NBSP is inserted instead of the space characters between **(a)**&nbsp;the shortenings of reference names (`Fig.`, `Figs.`, `Ref.`, `Refs.`, `Eq.`, `Eqs.`, `Sec.`, `P.`, and `p.`) and **(b)**&nbsp;a&nbsp;reference command despite the fact that it is preceded by&nbsp;`.`. These shortenings can be preceded by a&nbsp;newline&nbsp;(`\n`), the space or TAB character&nbsp;(`\t`), the opening brackets&nbsp;(`(`, `[`, and&nbsp;`{`; the latter means both the bracket itself&nbsp;`\{` and the beginning of&nbsp;`\command{...}`), and the opening quotes&nbsp;(`` ` ``,&nbsp;` `` `).

8. If a&nbsp;reference command is preceded by any post-spaced LaTeX `\command` without a&nbsp;closing brace (e.g., `{\bf \ref{fig}}`), no changes are made. This is because LaTeX normally ignores such spaces.

9. Also, the `typograph` function returns the found non-ASCII characters in order to help somebody who is required not to typeset such characters directly.

## What Can Go Wrong

1. `\tikz{\draw(0,0) -- (1,1)}` becomes `\tikz{\draw(0,0)~-- (1,1)}`.

2. `\includegraphics{1 -- 2.pdf}` becomes `\includegraphics{1~-- 2.pdf}`.

3. `to John Fig. \cite{wang2020} shows` becomes `to John Fig.~\cite{wang2020} shows` but Fig is a&nbsp;surname here and `\cite` starts a&nbsp;new sentence! However, it is generally accepted that a&nbsp;sentence should not start with a&nbsp;reference command. If you insert a&nbsp;noun, everything will be correct here: `to John Fig. Paper \cite{wang2020} shows` becomes `to John Fig. Paper~\cite{wang2020} shows`.

4. `(And he went out\ldots) \ref{fig} shows` becomes `(And he went out\ldots)~\ref{fig} shows` but this is wrong because `\cite` starts a&nbsp;new sentence. Again, insert a&nbsp;noun: then `(And he went out\ldots) Fig. \ref{fig} shows` becomes `(And he went out\ldots) Fig.~\ref{fig} shows`. Anyway, you should take care when typing the ellipsis (`...`, `\textellipsis`, `\dots`, or `\ldots`) which is quite an ambiguous thing in terms of regular expressions applied to the search of a&nbsp;sentence end.

5. And much more... This script plays rough. Be careful!

## Requirements

* Python 3.7 or later

* `regex` module (see [https://pypi.org/project/regex/](https://pypi.org/project/regex/))

## Changelog

* Version 1.0 (25 January 2021): initial release

----------

**LaTeX Typograph**

Version 1.0 (25 January 2021)

Copyright (c) 2021 Evgenii Shirokov

MIT License
