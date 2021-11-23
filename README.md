# parkrun_tokens
Generates replacement Parkrun finish tokens that can be printed and laminated to replace lost ones

Current Status
--------------

* Generates a working barcode that encodes P0001 etc. which can be scanned with the Virtual Volunteer App.
* Draws the barcode in a rectangle which is (about) the correct dimensions for the new (2020) style finish tokens, along with a marker for the hole.
* Writes "Hartlepool Parkrun" across the top.
* Takes a list of token numbers and arranges them on a single A4 page


Things to Do
------------
* Add a command line interface that takes a list of tokens and ranges (e.g 1-10,15,17,30-35)
* Handle generating multiple pages if necessary
* Provide command line options so other people can customise output without hacking the code.
* Tidy up the code - it uses python-barcode in quite a hacky way, using (supposedly) private members to access the xml to insert it into the page.
* Tidy up the code - it uses a modified version of the python-barcode SVGWriter.  It would be good to move the token drawing code out of there so we can
 use an unmodified SVGWriter to simplify the code further for ease of future maintenance.
 * Prettify the output - they look very ugly compared to the official Parkrun tokens!
