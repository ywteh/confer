#!/bin/bash
rm -rf *.aux
rm -rf *.bbl
rm -rf *.blg
rm -rf *.pdf
rm -rf *.log
echo "latexing"
pdflatex confer-hcomp-14.tex
bibtex confer-hcomp-14
echo "latexing once more"
pdflatex confer-hcomp-14.tex
pdflatex confer-hcomp-14.tex

echo "DONE"
