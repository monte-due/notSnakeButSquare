import pygame,sys,time,random,os
from pygame.locals import *
from ColorSet import *
from const import *
from welcomeScreen import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
#SGiocatore coprende i metodicomuni di player e proiettile
class SGiocatore:
	def printOnScreen(self,surface):
		pygame.draw.rect(surface,self.color,self.rect)
	def givePoint(self,player):
		player.pnt+=1
		effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","pointMade.wav"))
		effect.play()
		player.cura()
	def takePoint(self,player):
		effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","boom.wav"))
		effect.play()
		player.dimx-=danno
		player.dimy-=danno
		player.x=0
		player.y=0
		player.rect=pygame.Rect(player.x,player.y,player.dimx,player.dimy)
		player.pnt-=1
	def checkInObstacoleList(self,obsList):
		for x in obsList:
			if self.rect.colliderect(x.rect):
				return x.rect
	def checkCollide(self,player,enemy,obsList):
		if self.rect.colliderect(enemy.rect)and(self.color==enemy.color):
			enemy.generateNew(obsList)
			self.givePoint(player)
			return  True
		elif self.rect.colliderect(enemy.rect)and(self.color!=enemy.color):
			self.takePoint(player)
			return  True
		elif self.checkInObstacoleList(obsList):
			obsTuched=self.checkInObstacoleList(obsList)
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","obsTuch.wav"))
			effect.play()
			#se sta impattando dall' alto
			if self.y<obsTuched.y:
				self.y-=OFFSET
			#se sta impattando da sotto
			elif self.y>obsTuched.y:
				self.y+=OFFSET
			#da sx
			elif self.x<obsTuched.x:
				self.x-=OFFSET
			#da dx
			elif self.x>obsTuched.x:
				self.x+=OFFSET
			return True
		else:
			return False
	def checkGameOver(self):
		if ((self.dimx<=15) or (self.dimy<=15)):
			print 'morto'
			sayGoodBye(self.num)
	
#nemico comprende il nemico e gli ostacoli
class SNemico:
	def checkInObstacoleList(self,obsList):
		for x in obsList:
			if self.rect.colliderect(x.rect):
				return x.rect
	def printOnScreen(self,surface):
		pygame.draw.rect(surface,self.color,self.rect)
	def generateNewColor(self):
		numOfColor=numOfUsedColor
		listOfColor=[RED,YELLOW,BLUE,WHITE]
		newColor=listOfColor[random.randint(0,(numOfColor-1))]
		while newColor==self.color:
			newColor=listOfColor[random.randint(0,(numOfColor-1))]
		return newColor
	def generateNewXY(self,obsList):
		random.seed()
		x,y=0,0
		self.rect=pygame.Rect(x,y,25,25)
		while self.checkInObstacoleList(obsList):
			x=random.randint(0,MAXX-self.dimx)
			y=random.randint(0,MAXY-self.dimy)
			self.rect=pygame.Rect(x,y,25,25)
		return x,y
"""FINE SUPER CLASSI"""

#classe del giocatore
class Player(SGiocatore):
	def __init__(self,x,y,num):
		self.num=num
		self.x=x
		self.y=y
		self.pnt=0
		self.dimx=playerDimX
		self.dimy=playerDimY
		self.color=NAVYBLUE
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def changeColor(self,gameType):
		pressed=pygame.key.get_pressed()
		if gameType==1:
			if pressed[pygame.K_UP]:self.color=RED
			if pressed[pygame.K_DOWN]:self.color=BLUE
			if pressed[pygame.K_LEFT]:self.color=YELLOW
			if pressed[pygame.K_RIGHT]:self.color=WHITE
		else:
			if self.num==1:
				if pressed[pygame.K_SPACE]:self.color=RED
				if pressed[pygame.K_c]:self.color=BLUE
				if pressed[pygame.K_z]:self.color=YELLOW
				if pressed[pygame.K_x]:self.color=WHITE
			if self.num==2:
				if pressed[pygame.K_UP]:self.color=RED
				if pressed[pygame.K_DOWN]:self.color=BLUE
				if pressed[pygame.K_LEFT]:self.color=YELLOW
				if pressed[pygame.K_RIGHT]:self.color=WHITE
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def move(self,player,enemy,obsList,gameType):
		pressed=pygame.key.get_pressed()
		if gameType==1:
			if pressed[pygame.K_w]and(self.rect.y>=0):self.y-=OFFSET
			if pressed[pygame.K_s]and(self.rect.y<=MAXY-self.dimy):self.y+=OFFSET
			if pressed[pygame.K_a]and(self.rect.x>=0):self.x-=OFFSET
			if pressed[pygame.K_d]and(self.rect.x<=MAXX-self.dimx):self.x+=OFFSET
		else:	
			if self.num==1:
				if pressed[pygame.K_w]and(self.rect.y>=0):self.y-=OFFSET
				if pressed[pygame.K_s]and(self.rect.y<=MAXY-self.dimy):self.y+=OFFSET
				if pressed[pygame.K_a]and(self.rect.x>=0):self.x-=OFFSET
				if pressed[pygame.K_d]and(self.rect.x<=MAXX-self.dimx):self.x+=OFFSET		
			elif self.num==2:
				if pressed[pygame.K_i]and(self.rect.y>=0):self.y-=OFFSET
				if pressed[pygame.K_k]and(self.rect.y<=MAXY-self.dimy):self.y+=OFFSET
				if pressed[pygame.K_j]and(self.rect.x>=0):self.x-=OFFSET
				if pressed[pygame.K_l]and(self.rect.x<=MAXX-self.dimx):self.x+=OFFSET		
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def cura(self):
		if self.dimx<=dimWarn or self.dimy<=dimWarn:
			print 'stai per morire'
			self.dimx+=cure
			self.dimy+=cure
			self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)

#classe del proiettile
class Proiettile(SGiocatore):
	def __init__(self,player,Mdir):
		self.dimx=player.dimx/4
		self.dimy=player.dimy/4
		self.x=player.x+player.dimx/2.5
		self.y=player.y+player.dimy/2.5
		self.color=player.color
		self.Mdir=Mdir
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def shot(self,enemy,player,obsList,surface):
		tuched=False
		if self.Mdir==fireUP:
			while self.y>0:
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.y-=OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)	
		elif self.Mdir==fireDW:
			while self.y<MAXY :
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.y+=OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
		elif self.Mdir==fireSX:
			while self.x>0:
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.x-=OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
		elif self.Mdir==fireDX :
			while self.x<MAXX:
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.x+=OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)

"""classi derivate da SNemico"""
class Obstacole(SNemico):
	"""docstring for Obstacole"""
	def __init__(self):
		self.dimx=25
		self.dimy=25
		self.color=ORANGE
	def generateNew(self,obsList):
		self.x,self.y=self.generateNewXY(obsList)
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)

class Enemy(SNemico):
	def __init__(self):
		random.seed()
		self.dimx=15
		self.dimy=15
		self.color=None
	def generateNew(self,obsList):
		self.x,self.y=self.generateNewXY(obsList)
		self.color=self.generateNewColor()
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
