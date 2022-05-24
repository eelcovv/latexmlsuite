## Instructie maken plaatje met Python
 
Python script om een statisch plaatje in cbs huisstijl van de iris data te maken. Dit script 
schrijft ook de highcharts json template weg, zodat we direct een html kunnen maken om aan CCN aan
te leveren

Er worden 2 output files gemaakt:

1. het plaatje *afmetingen_bloem.pdf*. Dit plaatje kan je in je latex document importeren
2. de highcharts json file *afmetingen_bloem.json* onder de ccn output directory 
  *../../ccn/highcharts/hoofdstuk2/Fig_2_2_2*. 

Het nummer van de output map van de json file moet overeenkomen met het nummer dat het plaatje in 
je Latex document krijgt. Je kan de json file in highcharts importeren en vervolgens als html 
exporteren. Deze html zet je vervolgens naast de json in de map Fig_2_2_2, met de naam
*afmetingen_bloem.html*.

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
