# definieer de input en output directories
images_dir = .
highcharts_maindir = highcharts/hoofdstuk2
highcharts_dir = $(highcharts_maindir)/Fig_2_2_2
data_dir = ../../data

# definieer alle output file namen
file_base = afmetingen_bloem
pdf_file =  $(images_dir)/$(file_base).pdf
json_file =  $(highcharts_dir)/$(file_base).json

# definieer de input data files
data_in = $(data_dir)/$(file_base).csv

# definieer de script naam
script = plot_afmeting.py

# verzamel alle 'targets'
targets = $(pdf_file) $(json_file)

# verzamel alle 'dependencies'. Dus de targets hangen af van de ze files
dependencies = $(data_in) $(script)

# vanaf hier: specificeer de make regels

# default is de regel die je draait als je gewoon  'make' runt
default: all

# hier kan je meerdere regels verzamelen, als je meerdere plaatjes hebt
# we hebben nu maar 1 regel
all: afmetingen_bloem

# dit is de regel 'afmetingen_bloem' die  de 'targets' gaat maken
# hier specifier waar de targets door getriggerd worden. Als
# 1 van de dependencies nieuwer is dan 1 van de targets dan voor je de regel uit
# de regel die je uitvoert *moet* inspringen met een *tab*
afmetingen_bloem: $(targets)
$(targets): $(dependencies)
	python $(script)

clean:
	@$(foreach file, $(targets), test -f $(file) && rm -v $(file) || echo No $(file);)