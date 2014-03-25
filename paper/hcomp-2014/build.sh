#!/bin/bash
python gdoc2latex.py > confer-hcomp-14.tex
echo "latexing"
latex confer-hcomp-14.tex
echo "latexing once more"
latex confer-hcomp-14.tex

echo "creating the PDF using"
dvips -Ppdf -G0 -tletter confer-hcomp-14 -o confer-hcomp-14.ps
ps2pdf -sPAPERSIZE=letter -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=false -dEmbedAllFonts=true confer-hcomp-14.ps
cd ..

echo "DONE"
