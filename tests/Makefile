TESTS=Abs.elm Acos.elm Arg.elm Asin.elm Atan.elm Cos.elm Div.elm Exp.elm Ln.elm Mult.elm Pow.elm Sign.elm Sin.elm Sqrt.elm Tan.elm

all: $(TESTS)
	@make check_elm_test_installed
	@make check_testfiles_exist
	@for t in $(TESTS) ; do elm-test $$t && continue ; echo "$$t failed"; exit 1 ; done

check_elm_test_installed:
	@if ! type -p elm-test >/dev/null ; then echo "Can't find elm-test; please install it first"; exit 1; fi
	@if ! grep -qs elm-community/elm-test elm-package.json ; then echo "elm-test not initialized; please cd to the base dir of this package and run \"elm-test init\"" ; exit 1 ; fi

check_testfiles_exist:
	@for t in $(TESTS) ; do test -f $$t && continue ; make tests ; done

tests: $(TESTS)
	@./testgen-0.18.py

clean:
	rm -f $(TESTS)

clobber:
	rm -rf $(TESTS) Example.elm elm-package.json elm-stuff

.PHONY: $(TESTS)
