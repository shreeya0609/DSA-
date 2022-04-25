#19BEE0182, 19BEE0021, 20BEE0248, 20BEE0273, 19MIY0035

from turtle import exitonclick
import pygame
import random
import copy
from enum import Enum
from collections import namedtuple
import numpy as np
import sys
from os import path
from settings import *
#import chess_ff
import snakegame
import os
print("GAME CENTER")  
print("\nTEAM 8")
  
# creating options  
while True:  
    print("\nMAIN MENU")  
    print("1.CHESS")  
    print("2.SNAKEGAME")  
    print("3.PACMAN")  
    print("4.MINESWEEPER")
    print("5.SUDOKU SOLVER")
    print("6.EXIT")
    choice1 = int(input("Enter the Choice:"))  
  
    if choice1 == 1:  
        exec(open("19BEE0182_CHESSPROJECT/chess_ff.py").read())
      
    elif choice1 == 2:
        exec(open("19BEE0182_CHESSPROJECT/snakegame.py").read())

      
    elif choice1 == 3:  
        exec(open("19BEE0182_CHESSPROJECT/main.py").read())
    
    elif choice1 == 4:  
        exec(open("19BEE0182_CHESSPROJECT/Minesweeper.py").read())

    elif choice1 == 5:  
        exec(open("19BEE0182_CHESSPROJECT/GUI.py").read())
    
    elif choice1==6:
        break
      
    else:  
        print("Oops! Incorrect Choice.") 