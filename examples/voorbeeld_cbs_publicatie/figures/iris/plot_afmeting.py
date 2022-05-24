"""
Python script om een statisch plaatje in cbs huisstijl van de iris data te maken
"""
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from cbsplotlib.settings import CBSPlotSettings
from cbsplotlib.highcharts import CBSHighChart
from cbsplotlib.utils import add_axis_label_background

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)8s] %(message)s"
                    )
_logger = logging.getLogger(__name__)
figure_properties = CBSPlotSettings()


def make_bar_plot(data_df, im_name=None, y_label=None):
    """
    Make the bar plot van de data set

    Parameters
    ----------
    data_df: Dataframe
        pandas dataframe with the data
    im_name: str
        naam van het plaatje
    y_label: str
        Label van de y-as
    """

    # initieer plot
    fig, axis = plt.subplots(nrows=1, ncols=1)

    # plot data. Cbs stijl wil een ruimte tussen de bar van 0.75 pt. Los dit op door een witte rand
    data_df.plot(kind="bar", ax=axis, edgecolor="white", linewidth=0.75, rot=0, zorder=2)

    # pas de marges aan. We willen hier wat meer ruimte onderaan make
    fig.subplots_adjust(bottom=0.35)

    # Default zal matplotlib de hoogste bar boven het laatste grid punt door laten lopen
    # volgens de cbs richtlijnen moet de langste bar onder de hoogste ax waarde vallen
    # vraag hier de as waardes op met get_ytics en pas de y limiet hier op aan. Tel 0.01 op,
    # anders wordt de bovenste grid lijn dunner
    yticks = axis.get_yticks()
    axis.set_ylim((yticks[0], yticks[-1] + 0.05))

    axis.yaxis.grid(True)
    axis.tick_params(which="both", right=False, left=False)

    # y_label aan de linkboven. Tune de coordinaten om de label goed te positioneren
    axis.set_ylabel("Gemiddelde afmeting [mm]", rotation="horizontal",
                    horizontalalignment="left")
    axis.yaxis.set_label_coords(-0.04, 1.05)

    # xlabel boven aan horizontaal geplot
    axis.set_xlabel(data_df.index.name, rotation="horizontal", horizontalalignment="right")
    axis.xaxis.set_label_coords(0.95, -0.18)

    labels = [l.get_text() for l in axis.get_xticklabels()]
    axis.set_xticklabels(labels, ha='center')

    # haal de x-as weg, maar zet het verticale gris
    sns.despine(ax=axis, left=True)
    # haal de tick marks weg
    # pas de y-as dikte en kleur aan
    axis.spines["bottom"].set_linewidth(1.5)
    axis.spines["bottom"].set_color("cbs:highchartslichtgrijs")

    add_axis_label_background(fig, axes=axis, loc="south")

    # de legend aan de onderkant
    legend = axis.legend(loc="lower left",
                         bbox_to_anchor=(0.105, 0),
                         ncol=2,
                         bbox_transform=fig.transFigure,
                         frameon=False,
                         title="Bloemdeel")
    legend._legend_box.align = "left"

    _logger.info(f"Writing to {im_name}")
    fig.savefig(im_name)


def main():
    # de filename van de output
    csv_file = Path("../../data/afmetingen_bloem.csv")
    image_name = Path(csv_file.stem).with_suffix(".pdf")

    # laad de dataset
    geometry_df = pd.read_csv(csv_file, index_col=0)

    y_label = "Gemiddelde afmeting [mm]"

    # roep de plot functie aan voor het statische pdf plaatje
    make_bar_plot(data_df=geometry_df, im_name=image_name.as_posix(), y_label=y_label)

    # nu schrijven we de dataframe nog weg als json voor ccn
    ccn_out_dir = Path("../../ccn/highcharts/hoofdstuk2/Fig_2_2_2")
    ccn_out_dir.mkdir(exist_ok=True, parents=True)
    CBSHighChart(
        data=geometry_df,
        chart_type="column",
        xlabel=geometry_df.index.name,
        ylabel=y_label,
        y_lim=(0, 7),
        y_tick_interval=1,
        title="2.2.2 Gemiddelde afmeting per bloemonderdeel",
        output_file_name=image_name.stem,
        output_directory=ccn_out_dir.as_posix(),
    )


if __name__ == "__main__":
    main()
