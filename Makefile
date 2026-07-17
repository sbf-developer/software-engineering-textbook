.PHONY: pdf test clean

pdf:
	./scripts/build_pdf.sh

test:
	python3 -m unittest discover -s tests -v
	python3 scripts/verify_examples.py

clean:
	rm -rf build tmp/pdfs
	rm -f output/pdf/engineering-software.pdf output/pdf/engineering-software.pdf.sha256
