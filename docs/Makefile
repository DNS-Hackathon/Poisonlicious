all: draft-poisonlicious.txt draft-poisonlicious.html cache-poisonlicious-presentation.html

draft-poisonlicious.txt: ../draft-poisonlicious.xml
	xml2rfc --v3 -o $@ --text $<

draft-poisonlicious.html: ../draft-poisonlicious.xml
	xml2rfc --v3 -o $@ --html $<
	rm -f index.html
	ln -s $@ index.html

cache-poisonlicious-presentation.html: cache-poisonlicious-presentation.md
	marp $<
