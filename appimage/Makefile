.PHONY: default clean

UID := $(shell id -u $(USER))
GID := $(shell id -g $(USER))

default:
	sh build.sh

clean:
	rm build/*.rpm
