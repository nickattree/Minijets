# Minijets
A Python data analysis project using data from my thesis (available here http://qmro.qmul.ac.uk/jspui/handle/123456789/8915)

Minijets are sre small (~50km), linear features observed in Saturn's F ring and beleived to be casued by collisions with local moonlets. I have previously catalogued a number of them from images taken by the NASA Cassini spacecraft (details here http://arxiv.org/abs/1309.3119). The goal of this project is to rewrite my analysis code to make it freely available whilst teaching myself Python!

Cassini images are made public here https://pds.jpl.nasa.gov/ one year after being taken and all images used in this work satisfy this (see image use policy http://www.jpl.nasa.gov/copyrights.php). The data presented here is derived from Cassini images and is my own work which I am making availabe.

Files:

Minijets.csv    -     Comma seperated variable file containg measurements of each minijet feature and the image they were observed in

Series.csv      -     Comma seperated variable file containg details of the observations sequences the images are from

mj_readdata.py  -     Python code to read in the data, do some basic manipulation and plots

mj_timetrend.py  -    Python code to analyse time trends in minijet features

mj_morpho.py  -       Python code to analyse morphology of minijet features



