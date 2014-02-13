import pygame,sys,time,random,os
from newClass import *
from pygame.locals import *
from ColorSet import *
from  const import *

pygame.init()#inizlializzo pygame
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

fpsClock=pygame.time.Clock()#setto gli fps
surface=pygame.display.set_mode((MAXX,MAXY))#imposto il display
pygame.display.set_caption("NOT snake BUT square singleplayer")
pygame.mixer.music.load(os.path.join("src/snd/mp3/","base.mp3"))
pygame.mixer.music.play(-1)
gameType=1

def mostraPunti(player1,player2,surface):#stampa aschermo i punti del giocatore
	font=pygame.font.Font(pointFont,pointFontDim)
	pointDisplayG1=font.render("punti G"+str(player1.num)+": "+str(player1.pnt),1,GREEN)
	pointDisplayG1Postion=pointDisplayG1.get_rect()
	pointDisplayG1Postion.centerx=pointDisplayG1.get_rect().centerx
	pointDisplayG2=font.render("punti G"+str(player2.num)+": "+str(player2.pnt),1,RED)
	pointDisplayG2Postion=(MAXX/1.25,0)
	surface.blit(pointDisplayG1,pointDisplayG1Postion)
	surface.blit(pointDisplayG2,pointDisplayG2Postion)

def printObstacole(lista,surface):#stampa a schermo gli ostacoli
	for x in lista:
		x.printOnScreen(surface)	

def shotAnimation(player1,nemico,obsList,surface):#spara il proiettile
	pressed=pygame.key.get_pressed()

	if pressed[pygame.K_i]:
		raggioDellaMorte=Proiettile(player1,fireUP)
		raggioDellaMorte.shot(nemico,player1,obsList,surface)
			
	elif pressed[pygame.K_j]:
		raggioDellaMorte=Proiettile(player1,fireSX)
		raggioDellaMorte.shot(nemico,player1,obsList,surface)
			
	elif pressed[pygame.K_k]:
		raggioDellaMorte=Proiettile(player1,fireDW)
		raggioDellaMorte.shot(nemico,player1,obsList,surface)
			
	elif pressed[pygame.K_l]:
		raggioDellaMorte=Proiettile(player1,fireDX)
		raggioDellaMorte.shot(nemico,player1,obsList,surface)
			
def singlePlayer():
	

	#creo il giocatore ed il nemico
	player1=Player(0,0,1)
	nemico=Enemy()
	#genero gli ostacoli
	obstacoleList=[]
	for x in range(1,maxObs):
		x=Obstacole()
		x.generateNew(obstacoleList)
		obstacoleList.append(x)

	nemico.generateNew(obstacoleList)
	#contatore dei secondi prima di generare un nuovo nemico
	secondCounter=0

	while True:
		

		if secondCounter==new:
			nemico.generateNew(obstacoleList)
			secondCounter=0


		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit()

		
		player1.changeColor(gameType)
		player1.move(player1,nemico,obstacoleList,gameType)
		
		
		"""
		after that the player had move 
		the checkCollide method(called insede the move) control that the player, or is shot,
		is tuching an obstacol or the enemy, if is True it calculates the damneg
		check that the player don't walk above the obstacole 
		"""
		player1.checkGameOver()

		#parte "grafica"
		surface.fill(backgroundColor)
		printObstacole(obstacoleList,surface)
		mostraPunti(player1,player1,surface)
		player1.printOnScreen(surface)
		nemico.printOnScreen(surface)
		shotAnimation(player1,nemico,obstacoleList,surface)
		"""at th inside of the shot method there is the check of the collide of the shot"""
		

		
		pygame.display.update()
		fpsClock.tick(FPS)
		secondCounter+=1
