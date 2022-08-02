SOURCES := $(wildcard *.js)
JSONS := $(patsubst %.js,%.json,$(SOURCES))
COMPACTS := $(patsubst %.js,%-compact.json,$(SOURCES))

all: $(JSONS) $(COMPACTS)

# Appelle le parseur de Babel sur le code source
# Ce parseur est relativement lent, autant l’appeler une fois pour
# toute
$(JSONS): %.json: %.js
	babylon $< > $@

# Suppression du « bruit » (informations de localisation,
# commentaires, etc.) de l’AST
$(COMPACTS): %-compact.json: %.json
	jq 'del(.comments?) | del(.tokens?) | del(..|.start?) | del(..|.end?) | del(..|.loc?) | del (..|.extra?) | del(..|.leadingComments?) | del(..|.trailingComments?)' < $< > $@

clean:
	rm -rf *.json

.PHONY: all clean
