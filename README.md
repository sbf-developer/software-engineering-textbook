# Engineering Software

This repository contains the editable source, runnable examples, tests, and
build instructions for *Engineering Software: From Reliable Code to Production
Systems* by Scott Brodie Forsyth.

## Build the book

```sh
make pdf
```

The print-ready PDF is written to `output/pdf/engineering-software.pdf`.

## Run the examples and checks

```sh
make test
```

The checks use the Python standard library, Node.js, a C++ compiler, and the
system SQLite library. The Java example is deliberately dependency-free; if a
JDK is installed, compile it with:

```sh
javac examples/java/RetryPolicy.java
java -cp examples/java RetryPolicy
```

Docker and Docker Compose are optional. If available:

```sh
docker compose up --build
```

The Compose file follows the current Compose Specification style and runs the
small Python service used throughout the operational chapters.

## Source layout

- `book.tex` - master LaTeX document.
- `chapters/` - manuscript chapters.
- `examples/` - reference implementations in Python, TypeScript, Java, C++, SQL,
  and shell.
- `tests/` - executable checks for the examples.
- `references.bib` - bibliography with stable primary and official sources.
- `scripts/` - reproducible build and validation scripts.
- `.github/workflows/` - CI workflow for examples and PDF compilation.

This is educational material, not a security, legal, medical, or operational
guarantee. Adapt controls to the risks and obligations of the system being
built.

