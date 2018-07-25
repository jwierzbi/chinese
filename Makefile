# html:
#          xsltproc  \
#             --output  myfile.html  \
#             ../docbook-xsl-1.73.1/html/docbook.xsl  \
#             myfile.xml

# http://www.sagehill.net/docbookxsl/ParametersInFile.html
# http://www.sagehill.net/docbookxsl/SpecialChars.html
# http://stackoverflow.com/questions/2615002/how-to-generate-pdf-from-docbook-5-0
# http://www.javaranch.com/journal/200409/CreatingMultipleLanguagePDFusingApacheFOP.html
# http://www.sagehill.net/docbookxsl/SpecialChars.html

RELEASE ?= 0

OUTDIR := out
TARGET := characters.pdf
SOURCE := characters.xml

# ifeq ($(RELEASE),1)
PARAMS := --stringparam draft.mode no
# else
# PARAMS := --stringparam draft.mode yes
# endif

.PHONY = all
all: pdf

pdf: xml/$(SOURCE)
#	mkdir -p $(OUTDIR)
#	--stringparam symbol.font.family Arial --stringparam body.fontset "Arial"
#	xsltproc --output book.fo /usr/share/xml/docbook/stylesheet/docbook-xsl-ns/fo/docbook.xsl calibration.xml
	xsltproc $(PARAMS) --output $(OUTDIR)/$(SOURCE:.xml=.fo) config/wrapper.xml xml/$(SOURCE)
	fop -c config/fop.xml -fo $(OUTDIR)/$(SOURCE:.xml=.fo) -pdf $(OUTDIR)/$(TARGET)

.PHONY = clean
clean:
	rm -rf out
