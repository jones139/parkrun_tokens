#!/usr/bin/python


import gzip
import os
from typing import BinaryIO

import barcode

SIZE = barcode.writer.SIZE
COMMENT = barcode.writer.COMMENT


# A python-barcode writer that produces a barcode of the same dimensions
# as the new (2020) style finish tokens.
# Optional arguments w, h and r are the width, height and corner radius in
# mm.  Defaults are for the new size token.
class ParkrunTokenWriter(barcode.writer.BaseWriter):
    def __init__(self, w=55, h=25, r=3):
        self.w = w
        self.h = h
        self.r = r
        self.xOffset = 2.  # offset of barcode left from edge of token
        self.yOffset = 7.   # offset of barcode top from edge of token
        barcode.writer.BaseWriter.__init__(
            self, self._init,
            self._create_module, self._create_text, self._finish
        )
        self.compress = False
        self.with_doctype = False
        self._document = None
        self._root = None
        self._group = None

    def _init(self, code):
        width, height = self.calculate_size(len(code[0]), len(code))
        print("ParkrunTokenWriter._init() - width=%.1f, height=%.1f " % (width, height))
        self._document = barcode.writer.create_svg_object(self.with_doctype)
        self._root = self._document.documentElement
        attributes = {
            "width": SIZE.format(self.w),
            "height": SIZE.format(self.h),
        }
        print("ParkrunTokenWriter._init() - attributes=", attributes)
        barcode.writer._set_attributes(self._root, **attributes)
        if COMMENT:
            self._root.appendChild(self._document.createComment(COMMENT))

        # create group for easier handling in 3rd party software
        # like corel draw, inkscape, ...
        group = self._document.createElement("g")
        attributes = {"id": "barcode_group"}
        barcode.writer._set_attributes(group, **attributes)
        self._group = self._root.appendChild(group)

        background = self._document.createElement("rect")
        attributes = {
            "width": "100%",
            "height": "100%",
            "style": f"fill:{self.background}"
        }
        barcode.writer._set_attributes(background, **attributes)
        self._group.appendChild(background)

        tokenBorder = self._document.createElement("rect")
        attributes = {
            "width": SIZE.format(self.w),
            "height": SIZE.format(self.h),
            "rx": "3mm",
            "ry": "3mm",
            "style": f"fill:transparent; stroke:black; storke-width:3;"
        }
        barcode.writer._set_attributes(tokenBorder, **attributes)
        self._group.appendChild(tokenBorder)

        tokenHole = self._document.createElement("circle")
        attributes = {
            "cx": SIZE.format(self.w-7.6),
            "cy": SIZE.format(self.h/2.),
            "r": SIZE.format(2.2),
            "style": f"fill:transparent; stroke:black; storke-width:3;"
        }
        barcode.writer._set_attributes(tokenHole, **attributes)
        self._group.appendChild(tokenHole)

        element = self._document.createElement("text")
        attributes = {
            "x": SIZE.format(25),
            "y": SIZE.format(5),
            "style": "fill:{};font-size:{}pt;text-anchor:middle;".format(
                self.foreground,
                self.font_size,
            ),
        }
        barcode.writer._set_attributes(element, **attributes)
        text_element = self._document.createTextNode("Hartlepool Parkrun")
        element.appendChild(text_element)
        self._group.appendChild(element)


    def _create_module(self, xpos, ypos, width, color):
        element = self._document.createElement("rect")
        attributes = {
            "x": SIZE.format(xpos + self.xOffset),
            "y": SIZE.format(ypos + self.yOffset),
            "width": SIZE.format(width),
            "height": SIZE.format(self.module_height),
            "style": f"fill:{color};",
        }
        barcode.writer._set_attributes(element, **attributes)
        self._group.appendChild(element)

    def _create_text(self, xpos, ypos):
        # check option to override self.text with self.human (barcode as
        # human readable data, can be used to print own formats)
        if self.human != "":
            barcodetext = self.human
        else:
            barcodetext = self.text
        for subtext in barcodetext.split("\n"):
            element = self._document.createElement("text")
            attributes = {
                "x": SIZE.format(xpos + self.xOffset),
                "y": SIZE.format(ypos + self.yOffset),
                "style": "fill:{};font-size:{}pt;text-anchor:middle;".format(
                    self.foreground,
                    self.font_size,
                ),
            }
            barcode.writer._set_attributes(element, **attributes)
            text_element = self._document.createTextNode(subtext)
            element.appendChild(text_element)
            self._group.appendChild(element)
            ypos += barcode.writer.pt2mm(self.font_size) + self.text_line_distance

    def _finish(self):
        if self.compress:
            return self._document.toxml(encoding="UTF-8")
        else:
            return self._document.toprettyxml(
                indent=4 * " ", newl=os.linesep, encoding="UTF-8"
            )

    def save(self, filename, output):
        if self.compress:
            _filename = f"{filename}.svgz"
            f = gzip.open(_filename, "wb")
            f.write(output)
            f.close()
        else:
            _filename = f"{filename}.svg"
            with open(_filename, "wb") as f:
                f.write(output)
        return _filename

    def write(self, content, fp: BinaryIO):
        """Write `content` into a file-like object.

        Content should be a barcode rendered by this writer.
        """
        fp.write(content)



def makeTokensPage(tokensList):
    document = barcode.writer.create_svg_object(True)
    root = document.documentElement
    attributes = {
        "width": SIZE.format(210),
        "height": SIZE.format(297),
    }
    barcode.writer._set_attributes(root, **attributes)
    root.appendChild(document.createComment("Generated by finish_tokens.py"))
    xpos = 0
    ypos = 0
    for tokenVal in tokensList:
        print("making token: %s" % tokenVal)
        tokenCode = barcode.Code128(tokenVal, writer=ParkrunTokenWriter())
        tokenSvg = tokenCode.render(writer_options={"module_width":0.4,
                                                    "module_height":10.})
        print(tokenSvg)

        elem = document.createElement("svg")
        attributes= { "x": SIZE.format(xpos),
                      "y": SIZE.format(ypos)
        }
        barcode.writer._set_attributes(elem, **attributes)
        #node = document.createTextNode(tokenSvg.decode("utf-8"))
        #elem.appendChild(node)
        elem.appendChild(tokenCode.writer._root)

        root.appendChild(elem)
        xpos = xpos + 60
        if (xpos>210-60):
            xpos = 0
            ypos = ypos + 30

    svgTxt = document.toprettyxml(
        indent=4 * " ", newl=os.linesep, encoding="UTF-8"
    )
    #print(svgTxt)
    return(svgTxt)
        
def main():
    print("finish_tokens.main()")
    tokenVal = "P0001"
    #tokenCode = barcode.Code128(tokenVal, writer=barcode.writer.SVGWriter())
    #tokenCode.save("%s" % tokenVal)

    tokenVal = "P0002"
    #tokenCode = barcode.Code128(tokenVal, writer=ParkrunTokenWriter())
    #print("get_fullcode(): ",tokenCode.get_fullcode())
    #print(tokenCode.render())
    
    #tokenCode.save("%s" % tokenVal)

    # tokenPng = barcode.Code128(tokenVal, writer=barcode.writer.ImageWriter())
    # tokenPng.save(tokenVal)


    tokenLst = ["P0001", "P0002", "P0009"]
    svgTxt = makeTokensPage(tokenLst)

    outFile = open("tokenPage.svg","w")
    outFile.write(svgTxt.decode("utf-8"))
    outFile.close()

if (__name__ == "__main__"):
    main()
