Title: Graphics: Hexagon Grid
Date: 2016-09-09 16:27
Tags: Code
Category: Fun 
Slug:graphics-hexagon-grid

I have been learning about graphics. A language of choice would probably be OpenGL/WebGL but this
post would be in Java. Specifically, I would be using the [java.awt](https://docs.oracle.com/javase/7/docs/api/java/awt/package-summary.html) package. Most board games (chess, checkers ) use some sort of
grid based on some shape( squares, rectangles, hexagons are the most popular) for a playing surface. 


Today, I will be doing a hexagon grid. Hexagons can be either in a flat or pointy configuration. 


![Pointy vs Flat Orientation]({filename}../images/Point_flat_orientation.gif)


Rembering geometry `(SOHCAHTOH)`, the number of angles in a polygon `(n -2) * 180`  and some properties of equilateral 
triangles, we come up with this annotation:


![A annotated Pentagon]({filename}../images/Pentagon_annotated.jpg)


There are five vertices(I start from 0, because I am too used to `array notation`):

> $vert0 = ( x - \frac{r}{2}, y - \frac{h}{2})$
> 
> $vert1 = ( x + \frac{r}{2}, y - \frac{h}{2})$
> 
> $vert2 = ( x + r, y)$
> 
> $vert3 = ( x + \frac{r}{2}, y + \frac{h}{2})$
> 
> $vert4 = ( x - \frac{r}{2}, y + \frac{h}{2})$
> 
> $vert5 = ( x - r, y)$


We also need to get measurements for drawing rows and columns:


![Row measurements]({filename}../images/Row_annotated.jpg)


Other vertices:

> $vert6 = ( x + 2r, y)$
> 
> $vert7 = ( x + \frac{5r}{2}, y - \frac{h}{2})$
> 
> $vert8 = ( x + \frac{7r}{2}, y - \frac{h}{2})$
> 
> $vert9 = ( x + 4r, y)$
> 
> $vert10 = ( x - r, y + h)$


![Column measurements]({filename}/../images/Column_annotated.jpg)


The java code is shown below:


[gist:id=d65954e146db5738b7eb08953360f2e4]


Result on execution:


![Hexagon program execution]({filename}../images/hexagon_output.gif)


Something I might do in the future: 

* Rewrite in javafx
* Make it coloured
* Add a pointy example.


** Thanks!! **




