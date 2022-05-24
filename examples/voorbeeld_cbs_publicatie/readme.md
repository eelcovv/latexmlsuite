Deze repository kan je gebruiken als startpunt om een Latex publicatie maken

Je kan de volgende elementen terug vinden:

**Files**:

* *main.tex*:  dit is de master Latex file. Er wordt gebruik gemaakt van de Latex template 
  *cbsdocs* om pdf in publicatie formaat te maken 
* *AllMake*: Dit script kan je vanaf de bash shell runnen (onder linux) om de kopij te maken
* *AllMake.ps1*: Dit is gelijk aan het *AllMake* script, maar kan je vanaf de Powershell runnen 
  onder windows.
* *references.bib*: Hier kan je alle referenties van het document vastleggen.
* *.gitignore*: hier kan je vast leggen welke files niet in je git repository meegenomen mogen 
  worden.

**Mappen**:

* *data*: bevat input data die we gebruikt hebben om de voorbeeldplaatjes te maken 
* sections: bevat een latex file per hoofdstuk
* *figures*: bevat mappen met per map een plaatje. We hebben 2 voorbeeld mappen:
  
  * [*figures/iris*](https://github.cbsp.nl/EVLT/voorbeeld_cbs_publicatie/blob/master/figures/iris/readme.md): bevat een voorbeeld om een latex pdf + highcharts json mbv Python te maken. 
    Zie *figures/iris/readme.md* voor meer informatie
  * [*figures/iris_via_hc*](https://github.cbsp.nl/EVLT/voorbeeld_cbs_publicatie/blob/master/figures/iris_via_hc/readme.md): bevat een voorbeeld een plaatje in highcharts te maken en naar pdf te 
    converteren. Zie figures/iris_via_hc/readme.md voor meer informatie.
  
* *tables*: bevat een latex file per tabel