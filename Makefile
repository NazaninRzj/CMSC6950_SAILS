FIGURES= data.pdf fourier.pdf

report.pdf: report.tex ref.bib $(FIGURES) data_preparation.py Fourier_transform.py
	latexmk -pdf

data.pdf: data_preparation.py 911.csv
	python3 data_preparation.py

fourier.pdf:  Fourier_transform.py 911.csv
	python3 Fourier_transform.py

911.csv:
	unzip 100_1381403_bundle_archive.zip
	rm 100_1381403_bundle_archive.zip
	

.PHONY: clean almost_clean

clean: almost_clean
	rm  -f $(FIGURES)
	rm  -f report.pdf
	rm 911.csv

almost_clean:
	latexmk -c
	rm -rf data_preparation.py
	rm -rf Fourier_transform.py
	rm ref.bib
