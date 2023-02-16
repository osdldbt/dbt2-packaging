.PHONY: default clean

UID := $(shell id -u $(USER))
GID := $(shell id -g $(USER))

default:
	env UID=$(UID) GID=$(GID) docker-compose run --rm dbt2-appimage

clean:
	rm build/*.rpm
