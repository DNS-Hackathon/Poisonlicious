SOURCE  = \
	draft-bortzmeyer-dnsop-poisonlicious

all:	$(SOURCE).txt $(SOURCE).html

$(SOURCE).txt:	$(SOURCE).xml
	xml2rfc $(SOURCE).xml -n --text

$(SOURCE).html:	$(SOURCE).xml
	xml2rfc $(SOURCE).xml -n --html

$(SOURCE).xml:	$(SOURCE).md
	kramdown-rfc2629 $(SOURCE).md >$(SOURCE).new.xml
	mv $(SOURCE).new.xml $(SOURCE).xml

clean:
	rm -rf $(SOURCE).txt $(SOURCE).html
