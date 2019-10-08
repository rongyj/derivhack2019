PYTHON := pipenv run python
bot_version := $(shell pipenv run python src/python/setup.py --version)
dar := target/artifacts/dabl-hello.dar
bot := target/artifacts/dabl-hello-bot-$(bot_version).tar.gz

.PHONY: package
package: $(bot) $(dar)


$(dar):
	daml build -o $@


$(bot):
	cd src/python && $(PYTHON) setup.py sdist
	rm -fr src/python/dabl_hello_bot.egg-info
	mkdir -p $(@D)
	mv src/python/dist/dabl-hello-bot-$(bot_version).tar.gz $@
	rm -r src/python/dist

.PHONY: clean
clean:
	rm -fr src/python/dabl_hello_bot.egg-info src/python/dist target
