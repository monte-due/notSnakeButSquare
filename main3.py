import pygame,sys,time,random,os
sys.path.append("moduli/")
import welcomeScreen,singlePlayer,multyplayer
gameType=0
gameType=welcomeScreen.sayHello()
if gameType==1: 
	singlePlayer.singlePlayer()
if gameType==2:
	multyplayer.multiPlayer()
	