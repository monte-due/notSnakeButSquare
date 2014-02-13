import pygame,random,os
from pygame.locals import *
from ColorSet import *
from const import *
from welcomeScreen import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
#SGiocatore coprende i metodicomuni di player e proiettile
"""super classi"""
class SGiocatore:
	def printOnScreen(self,surface):#stampa a schermo il rettangolo in oggetto
		pygame.draw.rect(surface,self.color,self.rect)
	def givePoint(self,player):#attibuisce i punti al giocatore
		player.pnt+=1
		effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","pointMade.wav"))
		effect.play()
		player.cura()
	def takePoint(self,player):#se sbaglia colore toglie i punti
		effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","boom.wav"))
		effect.play()
		player.dimx-=danno
		player.dimy-=danno
		player.x=0
		player.y=0
		player.rect=pygame.Rect(player.x,player.y,player.dimx,player.dimy)
		player.pnt-=1
	def checkInObstacoleList(self,obsList):#controlla la collisione in ogni elemento della lista degli ostacoli
		for x in obsList:
			if self.rect.colliderect(x.rect):
				return x.rect#se collide ritorna il rettangolo
	def checkCollide(self,player,enemy,obsList,direction=None):#controlla la collisione
		if self.rect.colliderect(enemy.rect)and(self.color==enemy.color):#se collide con il nemico con il colore giusto
			enemy.generateNew(obsList)#genera un nuovo nemico
			self.givePoint(player)#attirbuisce i punti al giocatore
			return  True#ritorna dicente che c'e' stata una collisione
		elif self.rect.colliderect(enemy.rect)and(self.color!=enemy.color):#se collide con il nemico con il core sballato
			self.takePoint(player)#toglie i punti al giocatore
			return  True#ritorna dicendo che si e' avuto un nemico
		elif self.checkInObstacoleList(obsList):#se il controllo della collisione nella lista degli ostacoli ritorna un valore
			effect=pygame.mixer.Sound(os.path.join("src/snd/wav/","obsTuch.wav"))
			effect.play()
			print direction#stampa la direzione in cui e' avvenuto l' impatto
			#se sta impattando dall' alto
			if direction=="w":
				self.y+=OFFSET#abbassa il giocatore
			#se sta impattando da sotto
			elif direction=="s":
				self.y-=OFFSET#alza il giocatore
			#da sx
			elif direction=="a":
				self.x+=OFFSET#sposta a dx il, giocatore
			#da dx
			elif direction=="d":
				self.x-=OFFSET#sposta il giocatore a sx
			return True
		else:
			return False
	def checkGameOver(self):
		if ((self.dimx<=15) or (self.dimy<=15)):
			print 'morto'
			sayGoodBye(self.num)
	
#nemico comprende il nemico e gli ostacoli
class SNemico:
	def checkInObstacoleList(self,obsList):#controlla la collisione in ogni elemento della lista degli ostacoli
		for x in obsList:
			if self.rect.colliderect(x.rect):
				return x.rect
	def printOnScreen(self,surface):#stampa a achermo
		pygame.draw.rect(surface,self.color,self.rect)
	def generateNewColor(self):#genera un nuovo colore finche' non e' diverso da quello attuale
		numOfColor=numOfUsedColor
		listOfColor=[RED,YELLOW,BLUE,WHITE]
		newColor=listOfColor[random.randint(0,(numOfColor-1))]
		while newColor==self.color:
			newColor=listOfColor[random.randint(0,(numOfColor-1))]
		return newColor
	def generateNewXY(self,obsList):#genera nuovo cordinate xy
		random.seed()
		x=random.randint(0,MAXX-self.dimx*2)
		y=random.randint(0,MAXY-self.dimy*2)
		self.rect=pygame.Rect(x,y,25,25)
		while self.checkInObstacoleList(obsList):#controlla se il nuovo oggetto collide con un ostacolo preesistente
			x=random.randint(0,MAXX-self.dimx)
			y=random.randint(0,MAXY-self.dimy)
			self.rect=pygame.Rect(x,y,25,25)
		return x,y#dopo che le ha denerate ritorna le cordinate
"""FINE SUPER CLASSI"""

"""classi del giocaore"""
#classe del giocatore
class Player(SGiocatore):
	def __init__(self,x,y,num):
		self.num=num#id del giocatore
		#cordinate xy
		self.x=x
		self.y=y
		#punti fatti
		self.pnt=0
		#dimensioni
		self.dimx=playerDimX
		self.dimy=playerDimY
		#colore
		self.color=NAVYBLUE
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def changeColor(self,gameType):#cmabia il colore
		pressed=pygame.key.get_pressed()
		#i cotnrolli sono diversi da giocatore singolo e multiplayer
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
	def move(self,player,enemy,obsList,gameType):#moviemtno del giocatore
		pressed=pygame.key.get_pressed()#prende in input il tasto pemuto
		comando=None
		#anche qui doppi contrlli per singolo e multyplayer
		if gameType==1:
			#in single player oltra a muovere memorizza il tasto premuto
			if pressed[pygame.K_w]and(self.rect.y>=0):self.y-=OFFSET;comando="w"
			if pressed[pygame.K_s]and(self.rect.y<=MAXY-self.dimy):self.y+=OFFSET;comando="s"
			if pressed[pygame.K_a]and(self.rect.x>=0):self.x-=OFFSET;comando="a"
			if pressed[pygame.K_d]and(self.rect.x<=MAXX-self.dimx):self.x+=OFFSET;comando="d"
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
		self.checkCollide(player,enemy,obsList,comando)#dopo essersi mosso controlla evenutli collisioni 
	def cura(self):#cura
		if self.dimx<=dimWarn or self.dimy<=dimWarn:#se le dimensioni del gioatore sono pericolose la cura e' permessa
			print 'stai per morire'
			self.dimx+=cure
			self.dimy+=cure
			self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)#aggiorna il rettangolo

#classe del proiettile
class Proiettile(SGiocatore):
	def __init__(self,player,Mdir):
		#le dimensioni e cordinate eil colore dello sparo dipendono da quelle del giocatore
		self.dimx=player.dimx/4
		self.dimy=player.dimy/4
		self.x=player.x+player.dimx/2.5
		self.y=player.y+player.dimy/2.5
		self.color=player.color
		self.Mdir=Mdir#la direzione in cui andare dipende da quella del giocatore
		self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)
	def shot(self,enemy,player,obsList,surface):#funzione dello sparo
		tuched=False#per ora non ha toccato nulla
		if self.Mdir==fireUP:#se deve andare in alto
			while self.y>0:#finche' non tocca il limite dello schermo
				touched=self.checkCollide(player,enemy,obsList)#controlla collisioni
				if touched: break#se ci sono state interrompe
				self.y-=OFFSET#se non e' interrotto continua il movimento
				self.rect=pygame.Rect(self.x,self.y,self.dimx,self.dimy)#aggiorna il rettangolo
				self.printOnScreen(surface)#stampa aschermo il raggio
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
		self.color=obsColor
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
