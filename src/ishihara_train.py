import cv2
import math

img = cv2.imread('cb1.jpg') 

# for each test image
# ignore white, have dict with tuple as key and count as value
# return most common tuples
# these tuples form a set-when these colors are together it is a problem

counts = {}

for i in img:
    for j in i:
        working = tuple(j)

        w = int(working[0]) + int(working[1]) + int(working[2])

        if w < 750:      

            if working in counts:

                counts[working]= counts[working]+1

            else:

                addme = 0
                for key,val in counts.items():
                    if math.isclose(key[0],working[0],abs_tol=10) and \
                       math.isclose(key[1],working[1],abs_tol=10) and \
                       math.isclose(key[2],working[2],abs_tol=10):
                        counts[key] = val + 1

                        addme = 1
                if addme == 0:
                    counts[working]=1
                else:
                    addme = 0
##vals = []                             # this was for producing the test sets              
##for key,val in counts.items():        # and left in for completeness
##
##    if val > 500:
##        
##        vals.append(key)
