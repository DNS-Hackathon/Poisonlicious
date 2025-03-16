all: draft-poisonlicious.txt draft-poisonlicious.html

draft-poisonlicious.txt: ../draft-poisonlicious.xml
	xml2rfc -o $@ --text $<

draft-poisonlicious.html: ../draft-poisonlicious.xml
	xml2rfc -o $@ --html $<
	rm -f index.html
	ln -s $@ index.html
