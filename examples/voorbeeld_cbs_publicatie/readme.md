Deze repository kan je gebruiken als startpunt om een Latex publicatie maken

Je kan de volgende elementen terug vinden:

**Files**:

* *main.tex*:  dit is de master Latex file. Er wordt gebruik gemaakt van de Latex template 
  *cbsdocs* om pdf in publicatie formaat te maken 
* *references.bib*: Hier kan je alle referenties van het document vastleggen.
* *.gitignore*: hier kan je vast leggen welke files niet in je git repository meegenomen mogen 
  worden.
* *rapport_settings.yml*: input file voor *latex2ccn*, een Python script om zo efficient mogelijk
  de html kopij mbv latexml naar html om zet zetten.
* *maak_ccn_kopij.ps1*: een powershell script dat je kan runnen om alle kopij te maken.


**Mappen**:

* *data*: bevat input data die we gebruikt hebben om de voorbeeldplaatjes te maken 
* sections: bevat een latex file per hoofdstuk
* *figures*: bevat mappen met per map een plaatje. We hebben 2 voorbeeld mappen:
  
  * [*figures/iris*](https://github.cbsp.nl/EVLT/voorbeeld_cbs_publicatie/blob/master/figures/iris/readme.md): bevat een voorbeeld om een latex pdf + highcharts json mbv Python te maken. 
    Zie *figures/iris/readme.md* voor meer informatie
  * [*figures/iris_via_hc*](https://github.cbsp.nl/EVLT/voorbeeld_cbs_publicatie/blob/master/figures/iris_via_hc/readme.md): bevat een voorbeeld een plaatje in highcharts te maken en naar pdf te 
    converteren. Zie figures/iris_via_hc/readme.md voor meer informatie.
  
* *tables*: bevat een latex file per tabel


**Voorbereiding**

Om deze template voor de eerste keer te runnen moet je de volgende voorbereidingen treffen:

* Toegang tot *\\\\cbsp.nl\Productie\secundair\DecentraleTools\Output\CBS_Python*. Mocht je geen 
  rechten, dan kan je dat aanvragen bij [Henrico Witvliet](mailto:h.witvliet@cbs.nl)
* Vraag de volgende softwarepakketten aan bij TopDesk (als je ze nog niet hebt):
  
  - MikTex (voor het compileren van latex)
  - Git (voor het versiebeheer van je rapport)
  - Inkscape (om Highcharts plaatjes in statische .PDF om te zetten)
* Zorg dat je de volgende Network drives aanmaakt: 
  - *X:* &rarr; *\\\\cbsp.nl\Productie\secundair\DecentraleTools\Output\CBS_Python*
  - *Y:* &rarr; *\\\\cbsp.nl\infrastructuur\Apps\Centraal*
* Zorg dat je powershell profiel de goede instellingen heeft. Het makkelijkste is om het Powershell
  profiel onder *CBS_Python* (map *X:*) 
  *X:\share\data\scripts\Microsoft.PowerShell_profile.ps1* naar je 
  eigen directory *F:\Documents\WindowsPowerShell* te kopiëren.
 

**Maken voorbeeldpublicatie**

Als je de voorbereidingen hierboven gedaan hebt, kan je het volgende doen om dit voorbeeld 
te runnen

  * Open een Windows Powershell
  * Check of je profiel goed ingesteld is door op de powershell terminal te tikken:


    conda env list


  De uitvoer zou er zo uit moeten zien:


    # conda environments:
    #
    base                     \\cbsp.nl\Infrastructuur\Apps\Centraal\Python\python64_39
    cbs                   *  \\cbsp.nl\Infrastructuur\Apps\Centraal\Python\python64_39\envs\cbs

  Dit laat zien dat je inderdaad de Python 39 compiler goed in je pad hebt staan.

  * Ga naar een werkmap en clone de repository:


    cd F:\Documents\MijnRapporten
    git clone https://github.cbsp.nl/git/EVLT/voorbeeld_cbs_publicatie.git

  * Stap in de nieuw aangemaakte directory *voorbeeld_cbs_publicatie* en run alle code:


    cd voorbeeld_cbs_publicatie
    ./maak_ccn_kopij.ps1

Als alles klaar is zou je een nieuwe directory *ccn* moeten hebben met de kopij zoals je hem aan 
wilt leveren.  Deze kopij bevat het volgende:

* *voorbeeld_cbs_publicatie.pdf*: het pdf document dat je naast de long read kunt plaatsen.
* *highcharts*: directory met alle html grafieken zoals met highcharts gemaakt zijn.
* *html*: directory met alle html-files die CCN kan gebruiken om de kopij op te maken.
* *tabellen*: directory met alles xls-files voor de tabellen die je in je rapport hebt.