#!/bin/bash
rm -rf *.aux
rm -rf *.bbl
rm -rf *.blg
rm -rf *.pdf
rm -rf *.log
echo "preparing latex"
python gdoc2latex.py "https://docs.google.com/document/d/1sdXb8pCzEoZjrrndDiNROg7Q5wPvBiwA9vm3muiOnKQ/edit" > confer-hcomp-14.tex
echo "latexing"
pdflatex confer-hcomp-14.tex
bibtex confer-hcomp-14
echo "latexing once more"
pdflatex confer-hcomp-14.tex
pdflatex confer-hcomp-14.tex

#echo "creating the PDF using"
#dvips -Ppdf -G0 -tletter confer-hcomp-14 -o confer-hcomp-14.ps
#ps2pdf -sPAPERSIZE=letter -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=false -dEmbedAllFonts=true confer-hcomp-14.ps
#cd ..

echo "DONE"
