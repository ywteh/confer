#!/bin/bash
rm -rf *.aux
rm -rf *.bbl
rm -rf *.blg
rm -rf *.pdf
rm -rf *.log
echo "preparing latex"
python gdoc2latex.py "https://docs.google.com/document/d/1urtJuEFB4dVaqzYGtgrmkXsbRbg1jvFCnYnJl8OWG1M/edit" > confer-chi-15.tex
echo "latexing"
pdflatex confer-chi-15.tex
bibtex confer-chi-15
echo "latexing once more"
pdflatex confer-chi-15.tex
pdflatex confer-chi-15.tex
echo "DONE"
