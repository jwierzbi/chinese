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
CP = $(QUIET)cp
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
TARGET_XML := notes.xml

SOURCES_ARTICLES := \
	$(SRCDIR)/chapters/pinyin.xml

SOURCES_WORDS := \
	words.xml

SOURCES_CHARACTERS := \
	0001_0100.xml \
	0101_0200.xml \
	0201_0300.xml \
	0301_0400.xml

SOURCES_RADICALS := \
	radicals.xml

SOURCES := \
	$(SOURCES_WORDS) \
	$(SOURCES_CHARACTERS) \
	$(SOURCES_RADICALS)

PARAMS := --stringparam draft.mode no

.PHONY = all
all: pdf html

TARGET_PDF := notes.pdf
.PHONY = pdf
pdf: $(OUTDIR) $(OUTDIR)/$(TARGET_PDF)

$(OUTDIR)/$(TARGET_PDF): $(OUTDIR)/$(TARGET_PDF:.pdf=.fo)
	$(ECHO) "FOP $@"
	$(FOP) -c config/fop.xml -fo $< -pdf $@

$(OUTDIR)/$(TARGET_PDF:.pdf=.fo): $(OUTDIR)/$(TARGET_XML)
	$(XSLTPROC) $(PARAMS) --output $@ config/pdf_wrapper.xml $<

TARGET_HTML := index.htm
.PHONY = html
html: $(OUTDIR) $(OUTDIR)/$(TARGET_HTML)

$(OUTDIR)/$(TARGET_HTML): $(OUTDIR)/$(TARGET_XML) $(OUTDIR)/html_style.css
	$(XSLTPROC) $(PARAMS) --output $@ config/html_wrapper.xml $<

$(OUTDIR)/$(TARGET_XML): $(SOURCES_ARTICLES) $(addprefix $(OUTDIR)/,$(SOURCES))
	$(ECHO) "GEN2 $@"
	$(GEN2) -o $@ $^

$(OUTDIR)/%.css: config/%.css
	$(ECHO) COPY $@
	$(CP) $< $@

$(addprefix $(OUTDIR)/,$(SOURCES_WORDS)): $(OUTDIR)/%.xml:$(SRCDIR)/%.xml
	$(ECHO) GEN $@
	$(GEN) words -i $< -o $@ -c $(addprefix $(SRCDIR)/,$(SOURCES_CHARACTERS))

$(addprefix $(OUTDIR)/,$(SOURCES_CHARACTERS)): $(OUTDIR)/%.xml:$(SRCDIR)/%.xml
	$(ECHO) GEN $@
	$(GEN) characters -i $< -o $@ -r $(SRCDIR)/$(SOURCES_RADICALS)

$(addprefix $(OUTDIR)/,$(SOURCES_RADICALS)): $(OUTDIR)/%.xml:$(SRCDIR)/%.xml
	$(ECHO) GEN $@
	$(GEN) radicals -i $< -o $@

# Anki decks

.PHONY: anki
anki: anki_words anki_characters anki_radicals

TARGET_ANKI_WORDS := anki_words
.PHONY: anki_words
anki_words: $(OUTDIR) $(OUTDIR)/$(TARGET_ANKI_WORDS).txt

$(OUTDIR)/$(TARGET_ANKI_WORDS).txt: $(addprefix $(OUTDIR)/,$(SOURCES_WORDS:.xml=.txt))
	$(ECHO) Generating deck: $@
	$(CAT) $^ > $@

$(addprefix $(OUTDIR)/,$(SOURCES_WORDS:.xml=.txt)): $(OUTDIR)/%.txt:$(SRCDIR)/%.xml
	$(ECHO) GEN_ANKI $@
	$(GEN_ANKI) -i $< -o $@ -t words

TARGET_ANKI_CHARACTERS := anki_characters
.PHONY: anki_characters
anki_characters: $(OUTDIR) $(OUTDIR)/$(TARGET_ANKI_CHARACTERS).txt

$(OUTDIR)/$(TARGET_ANKI_CHARACTERS).txt: $(addprefix $(OUTDIR)/,$(SOURCES_CHARACTERS:.xml=.txt))
	$(ECHO) Generating deck: $@
	$(CAT) $^ > $@

$(addprefix $(OUTDIR)/,$(SOURCES_CHARACTERS:.xml=.txt)): $(OUTDIR)/%.txt:$(SRCDIR)/%.xml
	$(ECHO) GEN_ANKI $@
	$(GEN_ANKI) -i $< -o $@ -t chars

TARGET_ANKI_RADICALS := anki_radicals
.PHONY: anki_radicals
anki_radicals: $(OUTDIR) $(OUTDIR)/$(TARGET_ANKI_RADICALS).txt

$(OUTDIR)/$(TARGET_ANKI_RADICALS).txt: $(addprefix $(OUTDIR)/,$(SOURCES_RADICALS:.xml=.txt))
	$(ECHO) Generating deck: $@
	$(CAT) $^ > $@

$(addprefix $(OUTDIR)/,$(SOURCES_RADICALS:.xml=.txt)): $(OUTDIR)/%.txt:$(SRCDIR)/%.xml
	$(ECHO) GEN_ANKI $@
	$(GEN_ANKI) -i $< -o $@ -t radicals

# common targets

$(OUTDIR):
	$(MKDIR) out

.PHONY: clean
clean:
	$(ECHO) "removing out directory"
	$(RM) -rf out
