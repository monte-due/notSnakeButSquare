import pygame,sys,time,random,os
import ColorSet,welcomeScreen,const
from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

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
	def printOnScreen(self,surface):
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
	def printOnScreen(self,surface):
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
	def printOnScreen(self,surface):
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
	def printOnScreen(self,surface):
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

	def shot(self,Enemy,Player,surface):
		if self.Mdir==const.fireUP:
			while self.y>0 and not( self.rect.colliderect(Enemy.rect) ):
				self.y-=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)

		elif self.Mdir==const.fireDW:
			while self.y<const.MAXY and  not( self.rect.colliderect(Enemy.rect) ):
				self.y+=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)
				
		elif self.Mdir==const.fireSX  and not( self.rect.colliderect(Enemy.rect) ):
			while self.x>0 and not( self.rect.colliderect(Enemy.rect) ):
				self.x-=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)
					
		elif self.Mdir==const.fireDX :
			while self.x<const.MAXX and not( self.rect.colliderect(Enemy.rect) ):
				self.x+=10
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
				self.checkCollide(Enemy,Player)
				self.danno(Enemy,Player)