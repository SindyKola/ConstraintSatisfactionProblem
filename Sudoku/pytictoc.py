# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:08:41 2020

@author: Przemo
"""
import time

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

# This will be the main function through which we define both tic() and toc()
def toc(TicToc, tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
#        return ( "Elapsed time: %f seconds.\n" %tempTimeInterval )
        return tempTimeInterval

def tic(TicToc):
    # Records a time in TicToc, marks the beginning of a time interval
    toc(TicToc, False)