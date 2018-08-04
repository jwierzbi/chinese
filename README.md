# Chinese

My journey of learning Chinese.


## Generating PDF Document

### Prerequisites

This for sure works on Ubuntu 18.04.

    sudo apt install docbook5-xml docbook-xsl-ns xsltproc fop fonts-cns11643-kai

### Generating the Document

To generate the document:

    make

Files are placed in _out_ directory.

To clean generated files:

    make clean
