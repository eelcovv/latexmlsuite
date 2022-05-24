"""
Python scriptje om een csv file van de iris data te maken

Dit scriptje hoef je niet meer te draaien omdat de csv data bij de git repo gestopt is
Binnen de CBS omgeving werkt het niet vanwege de proxy (je haalt de data van een server), maar
thuis zou je kunnen doen:

python maak_iris_data.py

als je de files 'afmetingen_bloem.csv' en 'afmetingen_bloem.tex' wilt reproduceren.
"""
import logging

import seaborn as sns

# set de logger op
logging.basicConfig(level=logging.INFO, format="[%(levelname)8s] %(message)s")
_logger = logging.getLogger(__name__)


def main():
    # de filename van de output
    file_base = "afmetingen_bloem"
    csv_file = file_base + ".csv"
    xls_file = file_base + ".xlsx"
    tex_file = file_base + ".tex"

    # laad de dataset
    iris = sns.load_dataset('iris')
    _logger.info(f"\n{iris.head()}")

    # hernoem de kolommen
    iris.rename(columns={
        "sepal_length": "Stempellengte",
        "sepal_width": "Stempelbreedte",
        "petal_length": "Bladlengte",
        "petal_width": "Bladbreedte"
    }, inplace=True)

    #  bereken gemiddelde waardes
    geometry_df = iris.groupby("species").mean()

    # geef de index ook een naam
    geometry_df.index.name = "Bloemsoort"

    # de hele eerste kolom met bloemnamen willen met een hoofdletter laten beginnen
    geometry_df.index = geometry_df.index.str.capitalize()

    # schrijf alle data files
    geometry_df.to_csv(csv_file, float_format='%.1f')
    geometry_df.to_latex(tex_file, float_format='%.1f')


if __name__ == "__main__":
    main()
