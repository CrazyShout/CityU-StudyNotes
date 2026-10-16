# Embedded Chinese Unicode mapping

`Adobe-GB1-UCS2` is the unmodified Adobe mapping resource pinned by
`UPSTREAM.json`. Its header contains the copyright notice and BSD-3-Clause
license. The [upstream project](https://github.com/adobe-type-tools/mapping-resources-pdf)
maintains mappings used by PDF readers.

XeLaTeX embeds the Fandol font outlines but can omit a `ToUnicode` map for
registered Adobe-GB1 fonts. Readers without an external Adobe-GB1 language
pack can then omit the Chinese text altogether. `scripts/pdf_fonts.py`
embeds this resource during the normal publication build, before replacing
any published PDF. It does not replace glyphs, change text, or change layout.

Only the existing Identity-H / Adobe-GB1 encoding is handled. An unknown
composite font without a Unicode map fails the build. The standard validator
requires embedded composite fonts and Unicode maps and compares the Chinese
characters on every page using two independent PDF parsers.
