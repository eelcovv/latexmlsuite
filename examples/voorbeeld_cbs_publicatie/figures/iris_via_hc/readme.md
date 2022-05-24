## Instructie om Highcharts plaatje te maken

In deze directory hebben de het plaatje in highcharts zelf gemaakt
en hier als pdf  geconverteerd. 

De volgens stappen zijn gedaan:

1. **Maak je plaatje in highcharts.**

   - Importeer in highcharts de file *data/afmetingen_bloem.csv* (let op, kies ',' als *Delimiter* 
     en '.' als *Decimal Point Notation*)
   - Onder *Templates*: selecteer de *Column* template
   - Onder *Customize*:  voeg de as-labels en de titel van het plaatje toe. De titel moet 
     beginnen met het figuurnummer dat in het Latex document gebruikt wordt. In dit geval *2.2.1*. 
     Dit is hoe je het in de webpublicatie krijgt te zien.  
   
2. **Exporteer highcharts template *json* template file, de output file *svg*, en een *html* file:**

   - Onder *Export*: export als html door op de *export* knop te drukken
   - Met het *settingswieltje* doe: 
       - *Save Project*
       - *Export SVG for print*
   - Als je deze stappen gedaan hebt, heb je onder je *Downloads* maps 3 files aangemaakt:
     - *2.2.1 Gemiddelde afmeting per bloemonderdeel, plaatje gemaakt met highcharts.svg*
     - *221 Gemiddelde afmeting per bloemonderdeel plaatje gemaakt met highcharts.json*
     - *221_Gemiddelde_afmeting_per_bloemonderdeel_plaatje_gemaakt_met_highcharts_export.html*
     
3. **Kopieer de json, svg, en html file vanuit de *Downloads* map naar deze map:**

     - De html file is de file die we aan CCN aan gaan leveren. 
     - De json file heb je alleen nodig om nog eens iets aan te passen
     - De svg file moeten we nog naar pdf converteren om in latex te kunnen importeren
      
4. **Converteer de svg naar pdf met behulp van *Inkscape*:**

   - Importeer de svg file in *Inkscape*
   - Haal de titel van het plaatje weer weg, want deze gaan we in Latex met *caption* toevoegen
   - Sla de svg weer op onder een nieuwe naam door *Save as*: afmetingen_bloem_hc.svg
   - Ten slotte: sla de pdf op door *Save as* als:  afmetingen_bloem_hc.pdf

We kunnen deze pdf nu in latex importeren. 
    
We hebben in deze directory nog een makefile staan. Met deze Makefile zorgen we dat de html die
in deze directory opgeslagen staat naar de juiste highcharts directory gekopieerd wordt. Op die 
manier kunnen we makkelijk het pakketje met de aan te leveren file voor CCN maken.
Doe daarom helemaal nog aan het eind op de command line: *make*