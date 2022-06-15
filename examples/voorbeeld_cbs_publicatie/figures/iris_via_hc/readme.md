## Instructie om Highcharts plaatje te maken

In deze directory hebben het plaatje in highcharts zelf gemaakt en hier als pdf geconverteerd, zodat 
je het plaatje ook statisch in je Latex document kan meenemen. Hoewel je voor deze procedure geen
Python hoeft te gebruiken, is het uiteindelijk wel iets omslachtiger om te doen en zal het resultaat
in de latex publicatie er iets minder mooi uit zien. 

De volgens stappen zijn gedaan:

1. **Maak je plaatje in highcharts.**

   - Importeer in highcharts de file *data/afmetingen_bloem.csv* (let op, kies ',' als *Delimiter* 
     en '.' als *Decimal Point Notation*)
   - Onder *Templates*: selecteer de *Column* template
   - Onder *Customize*: voeg de as-labels en de titel van het plaatje toe. De titel moet 
     beginnen met het figuurnummer dat in het Latex document gebruikt wordt. In dit geval *2.2.1*. 
     Dit is hoe je het in de webpublicatie krijgt te zien.  
   
2. **Exporteer highcharts template *json* template file, de output file *svg*, en een *html* file:**
   - Maak een directory *highcharts/hoofdstuk2/Fig_2_2_1*
   - Onder *Export*: export als html door op de *export* knop te drukken
   - Met het *settingswieltje* doe: 
       - *Save Project*
       - *Export SVG for print*
   - Als je deze stappen gedaan hebt, heb je onder je *Downloads* maps 3 files aangemaakt:
     - *2.2.1 Gemiddelde afmeting per bloemonderdeel, plaatje gemaakt met highcharts.svg*
     - *221 Gemiddelde afmeting per bloemonderdeel plaatje gemaakt met highcharts.json*
     - *221_Gemiddelde_afmeting_per_bloemonderdeel_plaatje_gemaakt_met_highcharts_export.html*
     
3. **Kopieer de json, svg, en html file vanuit de *Downloads* map naar deze map:**

     - De html file is de file die we aan CCN aan gaan leveren. Verplaats deze daarom naar de map
      *highcharts/hoofdstuk2/Fig_2_2_1*, maar zorg wel dat je hem hernoemd, zodat de filenaam gelijk
      is aan de pdf file die we dadelijk in Latex gaan importeren: *afmetingen_bloem_hc.html*
     - De json file heb je alleen nodig om nog eens iets aan te passen. Sla hem daarom in de 
       directory op en voeg hem toe aan je repository.
     - De svg file moeten we nog naar pdf converteren om in latex te kunnen importeren. Sla hem 
       daarom ook op in deze directory en stop hem bij je repository
      
4. **Converteer de svg naar pdf met behulp van *Inkscape*:**

   - Importeer *2.2.1 Gemiddelde afmeting per bloemonderdeel, plaatje gemaakt met highcharts.svg* 
     in *Inkscape* (Inkscape kan je aanvragen via TopDesk)
   - Haal de titel van het plaatje weer weg, want deze gaan we in Latex met *caption* toevoegen
   - Sla de svg weer op onder een nieuwe naam door *Save as*: afmetingen_bloem_hc.svg
   - Ten slotte: sla de pdf op door *Save as* als:  afmetingen_bloem_hc.pdf. 
   - Voeg de pdf nu toe aan je latex document. Dit is terug te vinden in de file 
     gemiddelde_afmeting_hc.tex. Hierin moet je ook de caption nog eens zetten. 
    
5. **Synchroniseer je highcharts**
 
   - run het script *sync_htmls.ps1* om de html's onder je *highcharts* directory in dezelfde 
     directory structuur naar de *ccn* output directory in de root te kopieren. Deze stap hoef je
     niet zelf uit te voeren omdat dit ook al door *maak_ccn_kopij.ps1* gedaan wordt. 