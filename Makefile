FIGURES= data.pdf fourier.pdf

report.pdf: report.tex ref.bib $(FIGURES) sails_project.py
	latexmk -pdf

data.pdf: data_preparation.py 911.csv
	python3 data_preparation.py

fourier.pdf:  Fourier_transform.py 911.csv
	python3 Fourier_transform.py

911.csv:
	unzip 100_1381403_bundle_archive.zip
	rm 100_1381403_bundle_archive.zip
	cd 100_1381403_bundle_archive
	cp 911.csv ~/CMSC6950_SAILS/
	rm -rf 100_1381403_bundle_archive

.PHONY: clean almost_clean

clean: almost_clean
	rm  -f $(FIGURES)
	rm  -f report.pdf

almost_clean:
	latexmk -c
	rm -rf sails-example-data
