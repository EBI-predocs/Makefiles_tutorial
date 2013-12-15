# this is the first version of our Makefile

# definition of target and prerequesite: the "all" target is done when report.pdf exists
# the first target defined will be default (it will be called by typing just "make")
all: report.pdf

# example of an explicit build rule; the syntax is:
# target: prerequesites
#     shell commands (line needs to start with a TAB)
report.pdf: report.tex background.png interests_comp.png interests_wetlab.png correlations.png
	pdflatex report.tex report.pdf
	rm -f report.log report.aux

# another explicit build rule; this time, it uses a python script to produce a figure
background.png: plot_background.py Form_Responses.csv index.txt
	python plot_background.py background.png
	mogrify -resize 20% background.png
# Q: why do we list the script and the data as prerequesites?

# now, write rules to create the other .pngs with the plotting scripts
#
# TODO: insert code here

# ...

# it's always good to have a "clean" target that removes generated files
# to e.g. commit only the source files to VCS
clean:
	rm -f *.png *.pyc *.pdf
	rm -rf __pycache__

