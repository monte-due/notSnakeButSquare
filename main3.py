import pygame,sys,time,random,os
import ColorSet,welcomeScreen,const
from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

fpsClock=pygame.time.Clock()
surface=pygame.display.set_mode((const.MAXX,const.MAXY))
pygame.display.set_caption("NOT snake BUT square")
pygame.mixer.music.load(os.path.join("src/snd/mp3/","base.mp3"))
pygame.mixer.music.play(-1)

class Player(object):
	"""la classe che gestisce il giocatore"""
	def __init__(self,x,y,num):
		self.num=num
		self.x=x
		self.y=y
		self.pnt=0
		self.dimx=const.playerDimX
		self.dimy=const.playerDimY
		self.color=ColorSet.NAVYBLUE
		self.rect=pygame.Rect(x,y,self.dimx,self.dimy)
	def changeColor(self,gameType):
		pressed=pygame.key.get_pressed()
		if gameType==1:
			if pressed[pygame.K_UP]:self.color=ColorSet.RED
			if pressed[pygame.K_DOWN]:self.color=ColorSet.BLUE
			if pressed[pygame.K_LEFT]:self.color=ColorSet.YELLOW
			if pressed[pygame.K_RIGHT]:self.color=ColorSet.WHITE
		else:
			if self.num==1:
				if pressed[pygame.K_SPACE]:self.color=ColorSet.RED
				if pressed[pygame.K_c]:self.color=ColorSet.BLUE
				if pressed[pygame.K_z]:self.color=ColorSet.YELLOW
				if pressed[pygame.K_x]:self.color=ColorSet.WHITE
			if self.num==2:
				if pressed[pygame.K_UP]:self.color=ColorSet.RED
				if pressed[pygame.K_DOWN]:self.color=ColorSet.BLUE
				if pressed[pygame.K_LEFT]:self.color=ColorSet.YELLOW
				if pressed[pygame.K_RIGHT]:self.color=ColorSet.WHITE
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def move(self,gameType):
		pressed=pygame.key.get_pressed()
		if gameType==1:
			if pressed[pygame.K_w]and(self.rect.y>=0):self.MoveY(-const.OFFSET)
			if pressed[pygame.K_s]and(self.rect.y<=const.MAXY-self.dimy):self.MoveY(+const.OFFSET)
			if pressed[pygame.K_a]and(self.rect.x>=0):self.MoveX(-const.OFFSET)
			if pressed[pygame.K_d]and(self.rect.x<=const.MAXX-self.dimx):self.MoveX(+const.OFFSET)
		else:	
			if self.num==1:
				if pressed[pygame.K_w]and(self.rect.y>=0):self.MoveY(-const.OFFSET)
				if pressed[pygame.K_s]and(self.rect.y<=const.MAXY-self.dimy):self.MoveY(+const.OFFSET)
				if pressed[pygame.K_a]and(self.rect.x>=0):self.MoveX(-const.OFFSET)
				if pressed[pygame.K_d]and(self.rect.x<=const.MAXX-self.dimx):self.MoveX(+const.OFFSET)		
		if self.num==2:
				if pressed[pygame.K_i]and(self.rect.y>=0):self.MoveY(-const.OFFSET)
				if pressed[pygame.K_k]and(self.rect.y<=const.MAXY-self.dimy):self.MoveY(+const.OFFSET)
				if pressed[pygame.K_j]and(self.rect.x>=0):self.MoveX(-const.OFFSET)
				if pressed[pygame.K_l]and(self.rect.x<=const.MAXX-self.dimx):self.MoveX(+const.OFFSET)
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def MoveX(self,space):
		self.x+=space
	def MoveY(self,space):
		self.y+=space
	def printOnScreen(self):
		pygame.draw.rect(surface,self.color,self.rect)
	def checkCollide(self,Enemy):
		if self.rect.colliderect(Enemy.rect)and(self.color==Enemy.color):
			Enemy.generateNew()
			self.pnt+=1
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","pointMade.wav"))
			effect.play()
			if self.dimx<=const.dimWarn or self.dimy<=const.dimWarn:
				print 'stai per morire'
				self.dimx+=const.cure
				self.dimy+=const.cure
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def danno(self,Enemy):
		if self.rect.colliderect(Enemy.rect)and(self.color!=Enemy.color):
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","boom.wav"))
			effect.play()
			self.dimx-=const.danno
			self.dimy-=const.danno
			self.x=0
			self.y=0
			self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
			self.pnt-=1
	def checkCrash(self,Obstacole):
		if self.rect.colliderect(Obstacole.rect):
			#METTI SUONO RIMBALZO
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","obsTuch.wav"))
			effect.play()
			#se sta impattando dall' alto
			if self.y<Obstacole.y:
				self.y-=const.OFFSET
			#se sta impattando da sotto
			elif self.y>Obstacole.y:
				self.y+=const.OFFSET
			#da sx
			elif self.x<Obstacole.x:
				self.x-=const.OFFSET
			#da dx
			elif self.x>Obstacole.x:
				self.x+=const.OFFSET
	def checkGameOver(self):
		if ((self.dimx<=15) or (self.dimy<=15)):
			print 'morto'
			welcomeScreen.sayGoodBye(self.num)


class Enemy(object):
	"""classe per il nemicoEnemy"""
	def __init__(self):
		random.seed()
		dimx=15
		dimy=15
		x=random.randint(0,const.MAXX-dimx)
		y=random.randint(0,const.MAXY-dimy)
		numOfColor=4
		listOfColor=[ColorSet.RED,ColorSet.YELLOW,ColorSet.BLUE,ColorSet.WHITE]
		self.color=listOfColor[random.randint(0,(numOfColor-1))]
		self.rect=pygame.Rect(x,y,dimx,dimy)
	def generateNew(self):
		random.seed()
		dimx=15
		dimy=15
		x=random.randint(0,const.MAXX-dimx)
		y=random.randint(0,const.MAXY-dimy)
		numOfColor=4
		listOfColor=[ColorSet.RED,ColorSet.YELLOW,ColorSet.BLUE,ColorSet.WHITE]
		newColor=listOfColor[random.randint(0,(numOfColor-1))]
		while newColor==self.color:
			newColor=listOfColor[random.randint(0,(numOfColor-1))]
		self.color=newColor
		self.rect=pygame.Rect(x,y,dimx,dimy)
	def printOnScreen(self):
		pygame.draw.rect(surface,self.color,self.rect)
	

class Obstacole(object):
	"""docstring for Obstacole"""
	def __init__(self):
		self.dimx=25
		self.dimy=25
		self.color=ColorSet.ORANGE
	def generate(self):
		self.x=random.randint(self.dimx,const.MAXX-self.dimx)
		self.y=random.randint(self.dimy,const.MAXY-self.dimy)
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def printOnScreen(self):
		pygame.draw.rect(surface,self.color,self.rect)


class Proiettile(object):
	def __init__(self,Player,Mdir):
		self.dimx=Player.dimx/4
		self.dimy=Player.dimy/4
		self.x=Player.x+Player.dimx/2.5
		self.y=Player.y+Player.dimy/2.5
		self.color=Player.color
		self.Mdir=Mdir
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def printOnScreen(self):
		pygame.draw.rect(surface,self.color,self.rect)
	def checkCollide(self,Enemy,Player):
		if self.rect.colliderect(Enemy.rect)and(self.color==Enemy.color):
			Enemy.generateNew()
			Player.pnt+=1
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","pointMade.wav"))
			effect.play()
			if Player.dimx<=const.dimWarn or Player.dimy<=const.dimWarn:
				print 'stai per morire'
				Player.dimx+=const.cure
				Player.dimy+=const.cure
				Player.rect=pygame.Rect(Player.x,Player.y,Player.dimx,Player.dimy)
	def danno(self,Enemy,Player):
		if self.rect.colliderect(Enemy.rect)and(self.color!=Enemy.color):
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","boom.wav"))
			effect.play()
			Player.dimx-=const.danno
			Player.dimy-=const.danno
			Player.x=0
			Player.y=0
			Player.rect=pygame.Rect(Player.x,Player.y,Player.dimx,Player.dimy)
			Player.pnt-=1

	def shot(self,Enemy,Player):
		if self.Mdir==const.fireUP:
			while self.y>0 and not( self.rect.colliderect(Enemy.rect) ):
				self.y-=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen()
				pygame.display.update()
				fpsClock.tick(const.FPS)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)

		elif self.Mdir==const.fireDW:
			while self.y<const.MAXY and  not( self.rect.colliderect(Enemy.rect) ):
				self.y+=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen()
				pygame.display.update()
				fpsClock.tick(const.FPS)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)
				
		elif self.Mdir==const.fireSX  and not( self.rect.colliderect(Enemy.rect) ):
			while self.x>0 and not( self.rect.colliderect(Enemy.rect) ):
				self.x-=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen()
				pygame.display.update()
				fpsClock.tick(const.FPS)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)
					
		elif self.Mdir==const.fireDX :
			while self.x<const.MAXX and not( self.rect.colliderect(Enemy.rect) ):
				self.x+=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen()
				pygame.display.update()
				fpsClock.tick(const.FPS)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)
			



	


def mostraPunti(player1,player2):
	font=pygame.font.Font(const.pointFont,const.pointFontDim)
	pointDisplayG1=font.render("punti G"+str(player1.num)+": "+str(player1.pnt),1,ColorSet.GREEN)
	pointDisplayG1Postion=pointDisplayG1.get_rect()
	pointDisplayG1Postion.centerx=pointDisplayG1.get_rect().centerx
	pointDisplayG2=font.render("punti G"+str(player2.num)+": "+str(player2.pnt),1,ColorSet.RED)
	pointDisplayG2Postion=(const.MAXX/1.25,0)
	surface.blit(pointDisplayG1,pointDisplayG1Postion)
	surface.blit(pointDisplayG2,pointDisplayG2Postion)

def singlePlayer():
	
	obstacoleList=[]
	for x in range(1,const.maxObs):
		x=Obstacole()
		x.generate()
		obstacoleList.append(x)
	print obstacoleList
	pygame.display.set_caption("NOT snake BUT square singlePlayer")
	player1=Player(30,30,1)
	nemico=Enemy()
	secondCounter=0
	while True:
		if secondCounter==const.new:
			nemico.generateNew()
			secondCounter=0
		surface.fill(const.backgroundColor)
		mostraPunti(player1,player1)
		player1.printOnScreen()
		nemico.printOnScreen()
		for x in obstacoleList:
			x.printOnScreen()

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
		pressed=pygame.key.get_pressed()

		if pressed[pygame.K_i]:
			raggioDellaMorte=Proiettile(player1,"i")
			raggioDellaMorte.printOnScreen()
			raggioDellaMorte.shot(nemico,player1)
			
		if pressed[pygame.K_j]:
			raggioDellaMorte=Proiettile(player1,"j")
			raggioDellaMorte.printOnScreen()
			raggioDellaMorte.shot(nemico,player1)
			
		if pressed[pygame.K_k]:
			raggioDellaMorte=Proiettile(player1,"k")
			raggioDellaMorte.printOnScreen()
			raggioDellaMorte.shot(nemico,player1)
			
		if pressed[pygame.K_l]:
			raggioDellaMorte=Proiettile(player1,"l")
			raggioDellaMorte.printOnScreen()
			raggioDellaMorte.shot(nemico,player1)
			

		pygame.display.update()
		fpsClock.tick(const.FPS)
		secondCounter+=1

def multiPlayer():
	pygame.display.set_caption("NOT snake BUT square multiPlayer")
	enemy=Enemy()
	player1=Player(30,30,1)
	player2=Player(random.randint(0,const.MAXX/2),random.randint(0,const.MAXX/2),2)
	secondCounter=0
	while True:

		if secondCounter==const.new:
			enemy.generateNew()
			secondCounter=0
		surface.fill(const.backgroundColor)
		mostraPunti(player1,player2)
		player1.printOnScreen()
		player2.printOnScreen()
		enemy.printOnScreen()
	

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

#INIZIO PROGRAMMA		
#benvenuto
gameType=welcomeScreen.sayHello()
if gameType==1: 
	singlePlayer()
if gameType==2:
	multiPlayer()
	