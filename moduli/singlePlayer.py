import pygame,sys,time,random,os
import ColorSet,const
import classi
from pygame.locals import *
pygame.init()#inizlializzo pygame
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

fpsClock=pygame.time.Clock()#setto gli fps
surface=pygame.display.set_mode((const.MAXX,const.MAXY))#imposto il display
pygame.display.set_caption("NOT snake BUT square singleplayer")
pygame.mixer.music.load(os.path.join("src/snd/mp3/","base.mp3"))
pygame.mixer.music.play(-1)
gameType=1

def mostraPunti(player1,player2,surface):
	font=pygame.font.Font(const.pointFont,const.pointFontDim)
	pointDisplayG1=font.render("punti G"+str(player1.num)+": "+str(player1.pnt),1,ColorSet.GREEN)
	pointDisplayG1Postion=pointDisplayG1.get_rect()
	pointDisplayG1Postion.centerx=pointDisplayG1.get_rect().centerx
	pointDisplayG2=font.render("punti G"+str(player2.num)+": "+str(player2.pnt),1,ColorSet.RED)
	pointDisplayG2Postion=(const.MAXX/1.25,0)
	surface.blit(pointDisplayG1,pointDisplayG1Postion)
	surface.blit(pointDisplayG2,pointDisplayG2Postion)

def printObstacole(lista,surface):
	for x in lista:
		x.printOnScreen(surface)	
def shotAnimation(player1,nemico,surface):
	pressed=pygame.key.get_pressed()

	if pressed[pygame.K_i]:
		raggioDellaMorte=classi.Proiettile(player1,"i")
		raggioDellaMorte.shot(nemico,player1,surface)
			
	if pressed[pygame.K_j]:
		raggioDellaMorte=classi.Proiettile(player1,"j")
		raggioDellaMorte.shot(nemico,player1,surface)
			
	if pressed[pygame.K_k]:
		raggioDellaMorte=classi.Proiettile(player1,"k")
		raggioDellaMorte.shot(nemico,player1,surface)
			
	if pressed[pygame.K_l]:
		raggioDellaMorte=classi.Proiettile(player1,"l")
		raggioDellaMorte.shot(nemico,player1,surface)
			
def singlePlayer():
	
	#genero gli ostacoli e li stampo
	obstacoleList=[]
	for x in range(1,const.maxObs):
		x=classi.Obstacole()
		x.generate()
		obstacoleList.append(x)
	print obstacoleList

	#creo il giocatore ed il nemico
	player1=classi.Player(30,30,1)
	nemico=classi.Enemy()

	#contatore dei secondi prima di generare un nuovo nemico
	secondCounter=0

	while True:
		

		if secondCounter==const.new:
			nemico.generateNew()
			secondCounter=0


		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit()

		
		player1.changeColor(gameType)
		player1.move(gameType)
		player1.checkCollide(nemico)
		player1.danno(nemico)
		player1.checkGameOver()

		for x in obstacoleList:
			player1.checkCrash(x)

		surface.fill(const.backgroundColor)
		printObstacole(obstacoleList,surface)
		mostraPunti(player1,player1,surface)
		player1.printOnScreen(surface)
		nemico.printOnScreen(surface)

		shotAnimation(player1,nemico,surface)

		
		pygame.display.update()
		fpsClock.tick(const.FPS)
		secondCounter+=1
