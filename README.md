Makefile Tutorial
=================

### Why?

 * Lots of scripts in your directories
 * Describe *how* to call scripts (also for cluster computing)
 * Common interface to rerun your analysis
 * Works with all scripts that can be called from the command-line (not only R)

### How?

 * Have source files and target files
 * Write conversion rules (that use your scripts)
 * Run your entire workflow just by typing `make`
 * Have no additional work when the input data changes

### Prerequesites

You will need GNU make, pdflatex and Python incl. [pandas](http://pandas.pydata.org/) 
and [matplotlib](http://matplotlib.org/). Apart from the Python libraries, everything
should be installed on a Linux system.

On Mac, you will need the [command line tools](http://stackoverflow.com/questions/9329243/xcode-4-4-and-later-install-command-line-tools) of XCode.


Getting started: targets and prerequesites
------------------------------------------

```make
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

# now, write rules to create the other .pngs with the plotting scripts
#
# TODO: insert code here

# ...

# it's always good to have a "clean" target that removes generated files
# to e.g. commit only the source files to VCS
clean:
    rm -f *.png *.pyc *.pdf
```

**TODO:** write conversion rules to generate *.png* files from the other plotting scripts (remember that shell commands need to start with a TAB)

 * plot_interests_wetlab.py &#8594; interests_wetlab.png
 * plot_interests_comp.py &#8594; interests_comp.png
 * plot_correlations.py &#8594; correlations.png

When you have added the missing targets, your *Makefile* should run. Therefore, you can type `make` in a terminal and the default target (`all` in our case) is executed. If there is a prerequesite that is not available for `all` or outdated it is built before the target, and so on.

**Q:** for *background.png*, why do we list the script and the data as prerequesites?


Automatic and user-defined variables
------------------------------------

GNU make defines some variables automatically, like `$(MAKE)` for the make tool used or `$(HOME)` for the user home directory.

There are also rule-specific variables, for instance:
 * `$<` refers to the first prerequesite name
 * `$^` refers to all prerequesite names
 * `$@` refers to the target name
 * for a full list of implicit variables, see the [GNU make documentation](http://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html)

You can also define variables yourself, e.g.:

```make
SOURCE = Form_Responses.csv index.txt # reference this with $(SOURCE)
```

to refer to the source files, instead of having to reference them individually every time.

**TODO:** Add both make- and self-defined variables to reduce the redundancy in the Makefile.


Implicit conversion rules
-------------------------

Now that we have gotten rid of some redundancy and your *Makefile* should read approximately like this:

```make
SOURCE = Form_Responses.csv index.txt
SCRIPTS = plot_background.py plot_interests_comp.py plot_interests_wetlab.py plot_correlations.py
PLOTS = background.png interests_comp.png interests_wetlab.png correlations.png

all: report.pdf

report.pdf: report.tex $(PLOTS)
    pdflatex $< $@
    rm -f $*.log $*.aux

background.png: plot_background.py $(SOURCE) $(SCRIPTS)
    python $< $@
    mogrify -resize 20% $@

interests_comp.png: plot_interests_comp.py $(SOURCE) $(SCRIPTS)
    python $< $@
    mogrify -resize 20% $@

interests_wetlab.png: plot_interests_wetlab.py $(SOURCE) $(SCRIPTS)
    python $< $@
    mogrify -resize 20% $@

correlations.png: plot_correlations.py $(SOURCE) $(SCRIPTS)
    python $< $@
    mogrify -resize 20% $@

clean:
    rm -f *.png *.pyc *.pdf
```

What we still have got is a separate target for each of the plotting script calls. Wouldn't it be nice to write one rule that takes care of all the targets?

Turns out, we can do it using *implicit conversion rules*. If you want to convert all *.tex* files to *.pdf* files, the syntax is the following:

```make
%.pdf: %.tex $(PLOTS)
    # ...
```

The `%` is the magic character here. Your `all` target already knows that it needs to generate *report.pdf*, and this is the recipe how to generate any *.pdf* from a *.tex* file. `$(PLOTS)` is the same prerequesite as before.

**TODO:** Replace the 4 plotting rules by 1 implicit conversion rule.


File name matching and conversions
----------------------------------

If you like to get all file names in your current directory that match a specific pattern, you can use the `wildcard` macro:

```make
VARIABLE = $(wildcard *file*.ext)
```

Similarly, you can perform substitution operations on variables like this:

```make
VARIABLE = $(VARIABLE:%.ext=%.newext)
```

**TODO:** Use file name matching and substitution instead of enumerating your files in the `$(SCRIPTS)` and `$(PLOTS)` variables.


The final result
----------------

Once you are done, your *Makefile* should look similar to this:

```make
SOURCE = Form_Responses.csv index.txt
SCRIPTS = $(wildcard plot_*.py)
PLOTS = $(SCRIPTS:plot_%.py=%.png)

all: report.pdf
    
%.pdf: %.tex $(PLOTS)
    pdflatex $< $@
    rm -f $*.log $*.aux

%.png: plot_%.py $(SOURCE) $(SCRIPTS)
    python $< $@
    mogrify -resize 20% $@

clean:
    rm -f *.png *.pyc *.pdf
```

Follow up
---------

 * Detailed tutorial at Software carpentry: http://software-carpentry.org/v4/make/index.html
 * The GNU Make manual: http://www.gnu.org/software/make/manual/make.html

