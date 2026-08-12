.PHONY: pdf pdf-candidate check links check-labs clean

pdf:
	python3 build/build.py

pdf-candidate:
	STRIP_ANSWERS=1 python3 build/build.py

check:
	python3 build/linkify.py --check
	python3 build/check_book.py
	python3 build/check_diagrams.py chapters/*.md

links:
	python3 build/linkify.py

check-labs:
	@set -e; for d in labs/lab* exams/*/practical; do \
		[ -f "$$d/pyproject.toml" ] || continue; \
		echo "== $$d =="; \
		(cd "$$d" && uv sync --frozen -q && LAB_TARGET=solution uv run pytest -q -m "not live"); \
	done

clean:
	rm -rf dist
