# LaTeX Typograph

In LaTeX documents, this script replaces the space and/or tab characters with non-breaking spaces `~` before the spaced en and em dashes (`--`, `–`, `---`, and `—`) and reference commands (`\ref`, `\pageref`, `\eqref`, and `\cite`) using regular expressions. The `typograph(text: str)` function—the core part of this script—returns the improved LaTeX code (`str`) and the number of substitutions made (`int`). The script can mess up your document so be careful when using it (see details below).

## What It Can Do: Examples

| Input                                          | Output                                         |
|:-----------------------------------------------|:-----------------------------------------------|
| `Some scripts -- such this one -- are nice.`   | `Some scripts~-- such this one~-- are nice.`   |
| `Some scripts --- such this one --- are nice.` | `Some scripts~--- such this one~--- are nice.` |
| `Some scripts---such this one---are nice.`     | (no changes because the dashes are not spaced) |
| `As it is shown in \cite{wang2020}`            | `As it is shown in~\cite{wang2020}`            |
| `see Equation \eqref{sq}`                      | `see Equation~\eqref{sq}`                      |
| `on page \pageref{thm}`                        | `on page~\pageref{thm}`                        |
| `never before. \cite{wang2020} shows` | (generally no changes between `.,:;?!` and a reference) |
| `in Fig. \ref{fig}`                   | `in Fig.~\ref{fig}` (but `Fig.` allows `~`)             |
| `in {\bf \ref{fig}}`                  | (no changes between any `\command` and a reference)     |

## Details

1. It is supposed that your LaTeX document is initially prepared correctly. This script does not correct any typesetting mistakes. It just replaces the space and/or tab (ST) characters with the non-breaking space (NBSP) `~` where necessary.

2. Since LaTeX considers multiple consecutive ST characters as a single space character, this script works correctly if it finds such characters around dashes and before reference commands.

3. The ST characters are replaced with the NBSP before the spaced en/em dashes (`--`, `–`, `---`, and `—`) unless they start a new line or a file in general (because the leading whitespace characters in a line are ignored by LaTeX).

4. The NBSP is inserted instead of the ST characters between the reference command (`\ref`, `\pageref`, `\eqref`, and `\cite`) preceded by:
   - a Latin letter (`a`...`z`, `A`...`Z`) unless it is the last letter in any `\command` (because LaTeX normally ignores spaces after `\command`),
   - a digit (`0`...`9`),
   - a closing quote (`''`, `”`, `'`, or `’`) unless it is preceded by the end of a sentence (`.`, `?`, or `!`),
   - the percent sign in LaTeX `\%` (but not the comment `%`),
   - the dollar sign `$` (which means both USD `\$` and the end of inline equation `$...$`),
   - a closing bracket (`)` or `]`) unless it is preceded by the end of a sentence (`.`, `?`, or `!`),
   - the closing brace `}` (which means both the brace itself `\}` and the end of `\command{...}`).

5. For each reference command (`\ref`, `\pageref`, `\eqref`, and `\cite`), the allowed symbols that immediately follow it are specified in `refs` dictionary (lines 26–30). Generally, it is only `{` but both `{` and `[` are allowed after `\cite`.

6. Note that this script is supposed to be used if your bibliography citations appear as [1]. If it is something like [Wang, 2020], then the NBSP before it may be unnecessary but the script does not care about it. In such cases, you may want to remove `cite` key from `refs` dictionary (line 29).

7. If you are using any other bibliography citation commands (e.g., from `natbib` or `biblatex`) that produce citations like [1], you may want to add these commands to `refs` dictionary (lines 26–30).

8. Generally no changes are made if a reference command is preceded by a punctuation mark (`.,:;?!`) and the ST characters because the punctuation mark and the reference belong to logically different segments. The same goes for a preceding sentence in brackets or quotation marks (i.e., which ends with `.)`, `?''`, etc.).

9. However, the NBSP is inserted instead of the ST characters between the shortenings of reference names (`Fig.`, `Eqs.`, etc.) and a reference command. These shortenings are defined for each command in `refs` dictionary (lines 26–30) and can be preceded by:
   - the ST character,
   - file or newline beginning,
   - an opening bracket (`(`, `[`, or `{`; the latter means both the bracket itself `\{` and the beginning of `\command{...}`),
   - an opening quote (`` ` ``, `‘`, ` `` `, or `“`).

## What Can Go Wrong

1. `\tikz{\draw(0,0) -- (1,1)}` becomes `\tikz{\draw(0,0)~-- (1,1)}`.

2. `\includegraphics{1 -- 2.pdf}` becomes `\includegraphics{1~-- 2.pdf}`.

3. `...to John Fig. \cite{wang2020} shows...` becomes `...to John Fig.~\cite{wang2020} shows...` but Fig is a surname here and `\cite` starts a new sentence! However, it is generally accepted that a sentence should not start with a reference like [1]. If you insert a noun, everything will be correct here: `to John Fig. Paper \cite{wang2020} shows` becomes `to John Fig. Paper~\cite{wang2020} shows`.

4. The ellipsis (`...`, `\textellipsis`, `\dots`, or `\ldots`) may be not handled correctly.

5. And much more... This script plays rough. Be careful!

## Requirements

* Python 3.7 or later

* `regex` module (see [https://pypi.org/project/regex/](https://pypi.org/project/regex/))

## Changelog

* Version 2.0 (2021-03-24): add Unicode support

* Version 1.0 (2021-01-25): initial release

----------

**LaTeX Typograph**

Version 2.0 (2021-03-24)

Copyright (c) 2021 Evgenii Shirokov

MIT License
