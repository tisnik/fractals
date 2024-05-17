style-check:
	ruff .

type-checks:
	MYPYPATH=game: mypy --explicit-package-bases game

strict-type-checks:
	MYPYPATH=game: mypy --strict --explicit-package-bases demo

missing-types:
	MYPYPATH=game: mypy --explicit-package-bases --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs demo

demo.exe:
	python -m nuitka --follow-imports demo.py

