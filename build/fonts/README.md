# Vendored fonts — IBM Plex

The book renders in IBM Plex: Serif for body text, Sans for headings and tables,
Mono for code. The files live here on purpose.

**Why vendored, not installed.** WeasyPrint resolves a missing font silently.
A laptop without the font and a CI runner with it produce different PDFs, and
nothing in the build says so. These files make the output identical everywhere,
with no `apt` or `brew` step to keep in sync. `build/build.py` fails the build
if any file listed in `REQUIRED_FONTS` is absent.

Sans is a variable font; WeasyPrint instantiates the weight axis correctly
(verified: 400, 600 and 700 render at different widths).

**Licence.** IBM Plex is licensed under the SIL Open Font License 1.1.
`OFL.txt` is the licence text, and it permits redistribution inside this
repository. Source: the Google Fonts repository (`ofl/ibmplex*`).
