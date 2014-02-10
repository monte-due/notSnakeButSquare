import pygame,sys,time,random,os
import ColorSet,welcomeScreen,const
from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag


#giocatore coprende i metodicomuni di player e proiettile
class giocatore:
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
		player.dimx-=const.danno
		player.dimy-=const.danno
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
			enemy.generateNew()
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
				self.y-=const.OFFSET
			#se sta impattando da sotto
			elif self.y>obsTuched.y:
				self.y+=const.OFFSET
			#da sx
			elif self.x<obsTuched.x:
				self.x-=const.OFFSET
			#da dx
			elif self.x>obsTuched.x:
				self.x+=const.OFFSET
			return True
		else:
			return False
	def checkGameOver(self):
		if ((self.dimx<=15) or (self.dimy<=15)):
			print 'morto'
			welcomeScreen.sayGoodBye(self.num)
	
#nemico comprende il nemico e gli ostacoli
class nemico:
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

class Player(giocatore):
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
	def move(self,player,enemy,obsList,gameType):
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
	def cura(self):
		if self.dimx<=const.dimWarn or self.dimy<=const.dimWarn:
			print 'stai per morire'
			self.dimx+=const.cure
			self.dimy+=const.cure
			self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)

class Proiettile(giocatore):
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
		if self.Mdir==const.fireUP:
			while self.y>0:
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.y-=const.OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)	
		elif self.Mdir==const.fireDW:
			while self.y<const.MAXY :
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.y+=const.OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
		elif self.Mdir==const.fireSX:
			while self.x>0:
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.x-=const.OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)
		elif self.Mdir==const.fireDX :
			while self.x<const.MAXX:
				touched=self.checkCollide(player,enemy,obsList)
				if touched: break
				self.x+=const.OFFSET
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
				self.printOnScreen(surface)

class Obstacole(nemico):
	"""docstring for Obstacole"""
	def __init__(self):
		self.dimx=25
		self.dimy=25
		self.color=ColorSet.ORANGE
	def generateNew(self):
		self.x=random.randint(self.dimx,const.MAXX-self.dimx)
		self.y=random.randint(self.dimy,const.MAXY-self.dimy)
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)

class Enemy(nemico):
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