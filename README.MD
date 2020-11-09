# yahoo finance scraper 
takes input from a data.csv file with the symbol and description of the stock separated by tabs (\t)
and returns a csv file with yahoo's recommendation rating, price targets, performance outlook and if its undervalued or overvalued.
it uses selenium with chrome driver

# sample input
JAZZ	Jazz Pharmaceuticals Public Limited Company


# output
pizarra	descripcion	rating	current	average	low	high	valuacion	trend_short	trend_mid	trend_long
JAZZ	Jazz Pharmaceuticals Public Limited Company 02/09/2020	1.8	146.18	180.06	128.00	233.00	Overvalued	SUBE	SUBE	SUBE