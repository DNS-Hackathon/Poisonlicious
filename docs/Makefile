all: draft-poisonlicious.txt draft-poisonlicious.html

draft-poisonlicious.txt: ../draft-poisonlicious.xml
	xml2rfc --v3 -o $@ --text $<

draft-poisonlicious.html: ../draft-poisonlicious.xml
	xml2rfc --v3 -o $@ --html $<
	rm -f index.html
	ln -s $@ index.html
