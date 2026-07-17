#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/build"
OUT="$ROOT/output/pdf"
mkdir -p "$BUILD" "$OUT"

cd "$ROOT"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" book.tex >/tmp/engineering-software-pdflatex-1.log
cp references.bib "$BUILD/references.bib"
(cd "$BUILD" && bibtex book) >/tmp/engineering-software-bibtex.log
(cd "$BUILD" && makeindex book.idx) >/tmp/engineering-software-makeindex.log
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" book.tex >/tmp/engineering-software-pdflatex-2.log
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" book.tex >/tmp/engineering-software-pdflatex-3.log

cp "$BUILD/book.pdf" "$OUT/engineering-software.pdf"
pdfinfo "$OUT/engineering-software.pdf" | sed -n '1,20p'
sha256sum "$OUT/engineering-software.pdf" > "$OUT/engineering-software.pdf.sha256"
echo "Built $OUT/engineering-software.pdf"
