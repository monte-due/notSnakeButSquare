import pygame,sys,time,random,os
import ColorSet,welcomeScreen,const
import newClass,function
from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

fpsClock=pygame.time.Clock()
surface=pygame.display.set_mode((const.MAXX,const.MAXY))
pygame.display.set_caption("NOT snake BUT square")
pygame.mixer.music.load(os.path.join("src/snd/mp3/","base.mp3"))
pygame.mixer.music.play(-1)
gameType=2

def multiPlayer():
	pygame.display.set_caption("NOT snake BUT square multiPlayer")
	enemy=classi.Enemy()
	player1=classi.Player(30,30,1)
	player2=classi.Player(random.randint(0,const.MAXX/2),random.randint(0,const.MAXX/2),2)
	secondCounter=0
	while True:
		surface.fill(const.backgroundColor)

		if secondCounter==const.new:
			enemy.generateNew()
			secondCounter=0
		
		function.mostraPunti(player1,player2,surface)
		player1.printOnScreen(surface)
		player2.printOnScreen(surface)
		enemy.printOnScreen(surface)
	

		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit()

	
		player1.changeColor(gameType)
		player2.changeColor(gameType)
		player1.move(gameType)
		player2.move(gameType)
		player1.checkCollide(enemy)
		player2.checkCollide(enemy)
		player1.danno(enemy)
		player2.danno(enemy)
		player1.checkGameOver()
		player2.checkGameOver()

		pygame.display.update()
		fpsClock.tick(const.FPS)
		secondCounter+=1
