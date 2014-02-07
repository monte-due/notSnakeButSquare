import pygame,ColorSet,sys,const,os

def sayHello():
	pygame.init()
	
	surface = pygame.display.set_mode((const.MAXX,const.MAXY ))
	pygame.display.set_caption('hello surface')

	#imposto lo sfondo
	background=pygame.image.load(os.path.join('src/img/','welcome.jpg'))
	surface.fill(ColorSet.BLACK)

	# imposto i vari campi di testo
	font = pygame.font.Font(const.wclFont, const.wclFontDim)
	intestazione = font.render("Benvenuti", 1, ColorSet.BLUE)
	intestPostion = intestazione.get_rect()
	intestPostion.centerx = surface.get_rect().centerx

	singleplayer=font.render("w: singleplayer",1,ColorSet.RED)
	singleplayerPostion = surface.get_rect(center=((const.MAXX/2),(const.MAXY/2)))

	multiPlayer=font.render("p: multiplayer",1,ColorSet.RED)
	multiPlayerPostion=(const.MAXX/1.25,0)
	
	# Event loop
	while True:
		#metto a schermo i testi e lo sfondo
		surface.blit(background,(0,0))
		surface.blit(intestazione, intestPostion)
		surface.blit(singleplayer,singleplayerPostion)
		surface.blit(multiPlayer,multiPlayerPostion)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		pressed=pygame.key.get_pressed();
		if pressed[pygame.K_w]:return 1
		if pressed[pygame.K_p]:return 2
		if pressed[pygame.K_i]:
			spiegazione="prendi il quadratino piccolo usando il quadratone, il colore deve essere ==,cambialo con wasd"
			man=font.render(spiegazione,1,ColorSet.WHITE)
			manPostion=(0,const.MAXY/2)
			surface.blit(man,manPostion)
		pygame.display.update()

def sayGoodBye(playerID):
	pygame.init()
	surface = pygame.display.set_mode((const.MAXX,const.MAXY ))
	pygame.display.set_caption('DEATH SCREEN')

	#imposto lo sfondo
	background=pygame.image.load(os.path.join('src/img/','game-over.jpg'))
	surface.fill(ColorSet.BLACK)

	# imposto i vari campi di testo
	font = pygame.font.Font(const.wclFont, const.wclFontDim)
	addio = font.render("THE GAME giocatore " +str(playerID)+" invio per uscire", 1, ColorSet.BLUE)
	intestPostion = addio.get_rect()
	intestPostion.centerx = surface.get_rect().centerx
	while True:
		#metto a schermo i testi e lo sfondo
		surface.blit(background,  (const.MAXX/2-const.gameOverX/2,const.MAXY/2-const.gameOverY/2) )
		surface.blit(addio, intestPostion)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		pressed=pygame.key.get_pressed()
		if pressed[pygame.K_RETURN]:sys.exit()
		pygame.display.update()