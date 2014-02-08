import pygame,sys,time,random,os
sys.path.append("moduli/")
import welcomeScreen,singlePlayer,multyplayer

gameType=welcomeScreen.sayHello()
if gameType==1: 
	singlePlayer.singlePlayer()
if gameType==2:
	multyplayer.multiPlayer()
	