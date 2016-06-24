SOURCE = Form_Responses.csv index.txt
SCRIPTS = $(wildcard plot_*.py)
PLOTS = $(SCRIPTS:plot_%.py=%.png)

all: report.pdf

%.pdf: %.tex $(PLOTS)
	pdflatex $< $@
	rm -f $*.log $*.aux

%.png: plot_%.py $(SOURCE)
	python $< $@
	mogrify -resize 20% $@

clean:
	rm -f *.png *.pyc *.pdf
	rm -rf __pycache__

