import ishihara_cases as ic     # case1-case7, lens, cases
import cv2
import math
#import time
import sys
import os.path

#start = time.time()

def offensive(working,case):                                            # this finds if pixels being evaluated are close
                                                                        # to those in the test cases (and therefore
                                                                        # "potentially offensive")
    ret = 0
    for i in case:

       if math.isclose(i[0],working[0],abs_tol=10) and \
          math.isclose(i[1],working[1],abs_tol=10) and \
          math.isclose(i[2],working[2],abs_tol=10):
           ret += 1
           break                                                        # to avoid extra cycles and overfitting

    return ret

def evaluate_image(filename,flag):
    
    img = cv2.imread(filename)                                          # read in file

    if flag is '1':                                                     # warn user that this option is slow

        print('WARNING: Testing for potentially offensive pixels is VERY slow')

    cs = [set()]*7                                                      # records hits for test cases
    cs2 = [0]*7                                                         # counts number of hits for offensive pixels

    for i in img:                                                       #traverse rows
        for j in i:                                                     # traverse cols

            working = tuple(j)                                          # convert to tuple

            for i in range(7):

                if working in ic.cases[i]:                              # check items in test set
                    cs[i] = cs[i]|set({working})                        # add item to set

                if flag is '1':
                    
                    cs2[i]+=offensive(working,ic.cases[i])              # check for potentially offensive pixels
                    
    for i in range(7):

        sz = img.shape[0]*img.shape[1]                                  # total number of pixels in image
        cs[i] = round((len(cs[i])/ic.lens[i])*100)                             # what % of colors in test are in image
        cs2[i] = round((cs2[i]/sz)*100)                                        # % of offensive pixels

    for i in range(7):

        if flag is '1':                                                 # only print what's necessary based on tests selected
        
            print("Case",i+1,cs[i],"%",cs2[i],\
                  "% of pixels potentially offensive")
        else:
            print("Case",i+1,round(cs[i]),"%")

    cv2.imshow(filename,img)                                            # display image-mostly so keyboard commands will work

    #print('Elapsed time:',time.time()-start)                           # from testing
    
    while(True):                                                        # main program loop
        
        key = cv2.waitKey(10)
        
        if key == ord('q') or key == 27:                                # quit/exit
            cv2.destroyAllWindows()
            sys.exit()
        if key == ord('h'):                                             # help menu
            print('Controls:')
            print('q: Quit program')
            print('h: this help menu')
            print('v: Test for potentially offensive pixels-')
            print('  WARNING: VERY SLOW')
        if key == ord('v'):
            evaluate_image(filename,'1')                                # user can choose secondary test (not just at command line)
            
if len(sys.argv)>=2:                                                    # user specified input file
    if os.path.isfile(sys.argv[1]):                                     # checks for input file
        filename = sys.argv[1]
    else:
        raise NameError("File not found")                               # cannot find file

    if len(sys.argv)>=3:                                                # if user flagged to test for offensive pixels
        offenseflag = sys.argv[2]
        
    else:
        offenseflag = 0

    evaluate_image(filename,offenseflag)

elif len(sys.argv)<2:                                                   # no file specified, showing help

    print('Usage: python evaluate_image.py <filename> <TestOffensivePixelsFlag>')
    print('When TestOffensivePixelsFlag is set to 1, a secondary test (number of offensive pixels) is run')
    print('WARNING: Testing for potentially offensive pixels is VERY slow')
