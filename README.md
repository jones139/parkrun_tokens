# parkrun_tokens
We have an issue at our Parkrun with tokens going missing.  We have a nice set of new ones, so when we lose one we have to replace it with one of the old style ones...but we got the new set because the old ones were badly worn and difficult to scan.   We have some stickers to replace the worn barcodes, but these seem to wear out very quickly too.   So I decided to try to make some spares.

This programme generates replacement Parkrun finish tokens that can be printed and laminated to replace lost ones.   You give it a list or range of tokens you want to generate and it generates one or more Scaleable Vector Graphics (SVG) files that print on A4 that contain the requested tokens.

You can then print them, laminate them and cut them up ready for use.

<img src="https://raw.githubusercontent.com/jones139/parkrun_tokens/main/complete_set_of_tokens.jpg" width="400px">

Local Installation
------------
pip install python-barcode

No additional libraries or installation required - it runs from this directory.

Usage
-----

```
usage: finish_tokens.py [-h] [-f OUTFILE] [-t TITLE]
                        tokenListInput [tokenListInput ...]

positional arguments:
  tokenListInput        list of token numbers and ranges to generate (e.g 3 4
                        10-15 21-23 30)

optional arguments:
  -h, --help            show this help message and exit
  -f OUTFILE, --outFile OUTFILE
                        output filename (without extension) Default
                        'tokenPage'
  -t TITLE, --title TITLE
                        title to print on the top of each token
```

Example:

```
python finish_tokens.py -f output -t "Hartlepool Parkrun" 1 2 5-10 30
```

Will generate tokens 1, 2, 5, 6, 7, 8, 9, 10, 30 with title "Hartlepool Parkrun" and save the output as output_1.svg


The output looks like:

![output example](https://raw.githubusercontent.com/jones139/parkrun_tokens/main/example_output.png)

Print the generated .svg files, laminate and cut up to use as finish tokens.  

I found that a guillotine to cut the tokens into strips, then scissors to cut around each token worked well.  A standard hole punch can be used for the holes, but it takes a bit of practice to work out where to hold the token to punch the hole in the correct place.

We will have to see how hard wearing these are. The issue with the sticker barcode replacements is that they wore off quickly.  The approach I have used to laminate a whole sheet then cut it up results in un-sealed edges, so they may deteriorate in the rain.    Cutting before laminating would allow for sealed edges but would mean two cutting operations per token, so they will take nearly twice as long to make.


Current Status of Code
----------------------

* Generates a working barcode that encodes P0001 etc. which can be scanned with the Virtual Volunteer App.
* Draws the barcode in a rectangle which is (about) the correct dimensions for the new (2020) style finish tokens, along with a marker for the hole.
* Writes a given title across the top.
* Takes a list of token numbers and arranges them on one or more A4 pages as necessary.


Web Interface
-------------
Although running python scripts is trivial for us Linux/Unix users, that is
not the case for folks running Windows....  So to make it easier I have
created a simple web interface that runs the finish_tokens.py script
based on the text entered on a web page.

The Flask based web app is store in main.py and it is run within a Docker
container to (hopefully) make set-up and installation easier.

I can never remember docker commands so I have produced a Makefile that means
we can do:
  * make build - create a docker image that will run this web app.
  * make start - start a docker container running the image made with 'make build'
  * make stop - stop the container
  * make logs - list the output logs for debugging
  * make shell - log into the container so you can look around at what ishappening.

After doing 'make build' then 'make start' the web page should be visible at
http://localhost:56733
Entering the parkrun name and tokens to generate, then pressing the 'Submit' button shoudl result in a zip file being downloaded that contains the SVG images of the token pages.

Things to Do
------------
 * Prettify the output - they look very ugly compared to the official Parkrun tokens!   But I daren't put a parkrun logo on it in case I get complaints about using their branding....


Contact
-------
Graham Jones, grahamjones139@gmail.com

