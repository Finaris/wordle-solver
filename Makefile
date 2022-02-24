# Deals with creating py binaries and cleaning.

# Offloads most of the load to the script in bin.
# To modify what executables are made, edit the below file.
all:
	bin/.make_py_executables.sh	


# Removes generated cruft.
clean:
	rm -f Pipfile
	rm -f .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	cp bin/.make_py_executables.sh /tmp/
	rm -rf bin/
	mkdir bin
	mv /tmp/.make_py_executables.sh bin/

