# definieer de input en output directories
images_dir = .
highcharts_maindir = ../../ccn/highcharts/hoofdstuk2
highcharts_dir = ${highcharts_maindir}/Fig_2_2_1

# definieer alle output file namen
file_base = afmetingen_bloem_hc
html_file =  ${highcharts_dir}/${file_base}.html
html_original = 221_Gemiddelde_afmeting_per_bloemonderdeel_plaatje_gemaakt_met_highcharts_export.html

# verzamel alle 'targets'
targets = ${html_file}

# verzamel alle 'dependencies'. Dus de targets hangen af van de ze files
dependencies = ${html_original}

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
afmetingen_bloem: ${targets}
${targets}: ${dependencies}
	python -c "import pathlib; pathlib.Path('${highcharts_dir}').mkdir(parents=True, exist_ok=True)"
	python -c "import shutil; shutil.copyfile('${dependencies}', '${targets}')"

# bovenstaande python commando's zijn gebruikt om onderstaande regels onder powershell uit te voeren
#mkdir -pv ${highcharts_dir}
#cp -v ${dependencies}  ${targets}

clean:
	@$(foreach file, $(targets), test -f $(file) && rm -v $(file) || echo No $(file);)