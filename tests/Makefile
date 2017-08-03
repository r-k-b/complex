TESTS="Tests.elm"
ELM_RUNNER="TestsRunner.elm"
JS_RUNNER="testsRunner.js"

$(JS_RUNNER):
	python testgen.py $(TESTS) $(ELM_RUNNER)
	elm make $(ELM_RUNNER) --output $(JS_RUNNER)

test: $(JS_RUNNER)
	node $(JS_RUNNER)

.PHONY: test
