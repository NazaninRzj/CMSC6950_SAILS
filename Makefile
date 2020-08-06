FIGURES= F_M.pdf Real_Imag.pdf

report.pdf: report.tex $(FIGURES) sails_project.py
	latexmk -pdf

F_M.pdf: sails_project.py meg_occipital_ve.hdf5
	python3 sails_project.py

Real_Imag.pdf: sails_project.py meg_occipital_ve.hdf5
	python3 sails_project.py

meg_occipital_ve.hdf5:
	git clone https://vcs.ynic.york.ac.uk/analysis/sails-example-data

.PHONY: clean almost_clean

clean: almost_clean
	rm  -f $(FIGURES)
	rm  -f report.pdf

almost_clean:
	latexmk -c
	rm -rf sails-example-data
