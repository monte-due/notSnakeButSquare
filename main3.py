import pygame,sys,time,random,os
sys.path.append("moduli/")
import welcomeScreen
from singlePlayer import *
from multyplayer import *
gameType=0
gameType=welcomeScreen.sayHello()
if gameType==1: 
	singlePlayer()
if gameType==2:
	multiPlayer()
	