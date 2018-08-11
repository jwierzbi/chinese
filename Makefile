# http://www.sagehill.net/docbookxsl/ParametersInFile.html
# http://www.sagehill.net/docbookxsl/SpecialChars.html
# http://stackoverflow.com/questions/2615002/how-to-generate-pdf-from-docbook-5-0
# http://www.javaranch.com/journal/200409/CreatingMultipleLanguagePDFusingApacheFOP.html
# http://www.sagehill.net/docbookxsl/SpecialChars.html


VERBOSE ?= 0

ifeq ($(VERBOSE),1)
QUIET=
else
QUIET=@
endif

# tools

ECHO = @echo
CAT = $(QUIET)cat
RM = $(QUIET)rm
MKDIR = $(QUIET)mkdir
XSLTPROC = $(QUIET)xsltproc
FOP = $(QUIET)fop
GEN = $(QUIET)tools/gen_docbook.py
GEN2 = $(QUIET)tools/gen_article.py
GEN_ANKI = $(QUIET)tools/gen_ankideck.py

# config

SRCDIR := xml
OUTDIR := out
TARGET := characters

SOURCES := \
	0001_0100.xml \
	0101_0200.xml \
	radicals.xml

PARAMS := --stringparam draft.mode no

.PHONY = all
all: pdf html

.PHONY = pdf
pdf: $(OUTDIR) $(OUTDIR)/$(TARGET).pdf

$(OUTDIR)/$(TARGET).pdf: $(OUTDIR)/$(TARGET).fo
	$(ECHO) "FOP $@"
	$(FOP) -c config/fop.xml -fo $< -pdf $@

$(OUTDIR)/$(TARGET).fo: $(OUTDIR)/$(TARGET).xml
	$(XSLTPROC) $(PARAMS) --output $@ config/pdf_wrapper.xml $<

.PHONY = html
html: $(OUTDIR) $(OUTDIR)/$(TARGET).htm

$(OUTDIR)/$(TARGET).htm: $(OUTDIR)/$(TARGET).xml
	$(XSLTPROC) $(PARAMS) --output $@ config/html_wrapper.xml $<

$(OUTDIR)/$(TARGET).xml: $(addprefix $(OUTDIR)/,$(SOURCES))
	$(ECHO) "GEN2 $@"
	$(GEN2) -o $@ $^

$(OUTDIR)/%.xml: xml/%.xml
	$(ECHO) GEN $@
	$(GEN) -i $< -o $@

.PHONY = anki
anki: $(OUTDIR) $(OUTDIR)/anki_$(TARGET).txt

$(OUTDIR)/anki_$(TARGET).txt: $(addprefix $(OUTDIR)/,$(SOURCES:.xml=.txt))
	$(ECHO) Generating deck: $@
	$(CAT) $^ > $@

$(OUTDIR)/%.txt: $(SRCDIR)/%.xml
	$(ECHO) GEN_ANKI $@
	$(GEN_ANKI) -i $< -o $@

$(OUTDIR):
	$(MKDIR) out

.PHONY = clean
clean:
	$(ECHO) "removing out directory"
	$(RM) -rf out
