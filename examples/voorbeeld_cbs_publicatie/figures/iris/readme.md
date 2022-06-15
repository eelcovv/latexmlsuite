## Instructie maken plaatje met Python
 
Python script om een statisch plaatje in cbs huisstijl van de iris data te maken. Dit script 
schrijft ook de highcharts json template weg, zodat we direct een html kunnen maken om aan CCN aan
te leveren

Er worden 2 output files gemaakt:

1. het plaatje *afmetingen_bloem.pdf*. Dit plaatje kan je in je latex document importeren
2. de highcharts json file *afmetingen_bloem.json* wordt naar de highcharts directory geschreven
  *highcharts/hoofdstuk2/Fig_2_2_2*. 

Het nummer van de output map van de json file moet overeenkomen met het nummer dat het plaatje in 
je Latex document krijgt. Je kan de json file in highcharts importeren en vervolgens als html 
exporteren. Deze html zet je vervolgens naast de json in de map Fig_2_2_2, met de naam
*afmetingen_bloem.html*. 

De json stop je niet in de repository (wordt ignored), omdat dit een door het script gegenereerde 
file is. De html die je vanuit Highcharts exporteert stop je wel in de repository om te voorkomen 
dat je ze kwijt raakt; het kost moeite om json naar html om te zetten. Het sync_htmls.ps1 script 
zullen alle htmls synchroniseren met de ccn output directory. Het sync_htmls.sh script kan je 
gebruiken als je onder Linux werkt. Het aanroepen van het script wordt door *latex2ccn* gedaan.

Om de plaatjes te maken moet je het script *plot_afmetingen.py* runnen. Je hebt hiervoor 
twee manieren:

1. In pycharm:

   - selecteer 'plot_afmeting.py' en doe rechtermuisknop Run 'plot_afmeting.py'
 
2. Op de command line:

   - type in: *python plot_afmeting.py*
   - *OF* type in: *make*

Het voordeel van de make methode is dat je script alleen gerund wordt als je
script of de csv input file nieuwer is dan de output files 
(het pdf plaatje en de highcharts json file)

##### Stappen die je moet doen om de plaatjes via de Python route te maken

1. Als je *maak_ccn_kopij.ps1* in de root directory runt wordt automatisch het volgende gedaan: 
    - De Makefile wordt gelanceerd met *make*
    - Hierdoor draait het pythonscript *plot_afmeting.py* alleen als dat nodig is.
    - Het pdf plaatje *afmeting_bloem.pdf* wordt gemaakt om in Latex te kunnen importeren. Het 
      importeren kan je in *gemiddelde_afmeting.tex* terugvinden. 
    - De *Highcharts* json wordt gemaakt waarme we hetzelfde plaatje naar CCN kunnen aanleveren. 
      De json moeten we de volgende stap echter zelf nog naar html converteren mvb Highcharts.
2. Nadat je de eerste keer *maak_ccn_kopij.ps1* gerund hebt, vind je onder de directory 
   *figures/iris/highcharts/hoofdstuk2/Fig_2_2_2* de file *afmeting_bloem.json* terug. Je moet nu
    eenmalig per figuur het volgende doen:
   - Importeer deze file in Highcharts, ga gelijk naar de *Export* tab en druk op de *Export* knop. 
     Er wordt een html file *222_Gemiddelde_afmeting_per_bloemonderdeel_export.html* naar je  
     *F:\Downloads* directory geschreven. 
   - Verplaats deze file naast de json file in de *Fig_2_2_2* directory en hernoem hem gelijk
     aan de json file, in dit geval *afmeting_bloem.html*. Het figuurnummer kan CCN aflezen aan de naam
     van de directory (*Fig_2_2_2*); je wilt hier juist exact dezelfde naam als de pdf file die je in 
     Latex importeert (*afmeting_bloem.pdf*), omdat deze filenaam in de kopij html file die je aan
     CCN gaat aanleveren als verwijzing wordt laten zien.
   - Als dit de eerste keer is dat je de html maakt, moet je de file nog aan de git repository
     toevoegen zodat je werk om de html file te maken niet verloren gaat.
3. Run nu het script *sync_htmls.ps1*. Hierdoor worden alle html-files onder highcharts naar de
   *ccn* directory onder de root directory gekopieerd in dezelfde directory structuur als je onder
   de *highcharts* directory aangemaakt hebt. Op deze manier lever je als je highcharts plaatjes
   aan, met ieder plaatje in een directory die de naam van het figuurnummer aangeeft.  
4. In principe hoef je *sync_htmls.ps* niet zelf te runnen omdat dit al door *maak_ccn_kopij.ps1* 
   gedaan wordt. Het enige dat je als gebruiker doet is dus: 1) run *maak_ccn_kopij.ps1*, 2) 
   converteer de json files in html met Highcharts zoals hierboven beschreven en stop hem bij
   de git repository, en 3) run *maak_ccn_kopij.ps1* nogmaals om ook alle htmls te synchroniseren. 
   Mocht je geen nieuwe htmls hebben dan hoef je alleen eenmalig *maak_ccn_kopij.ps1* te runnen.
  
