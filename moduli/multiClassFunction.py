import pygame
import const,ColorSet
pygame.init()

def mostraPunti(player1,player2,surface):
	font=pygame.font.Font(const.pointFont,const.pointFontDim)
	pointDisplayG1=font.render("punti G"+str(player1.num)+": "+str(player1.pnt),1,ColorSet.GREEN)
	pointDisplayG1Postion=pointDisplayG1.get_rect()
	pointDisplayG1Postion.centerx=pointDisplayG1.get_rect().centerx
	pointDisplayG2=font.render("punti G"+str(player2.num)+": "+str(player2.pnt),1,ColorSet.RED)
	pointDisplayG2Postion=(const.MAXX/1.25,0)
	surface.blit(pointDisplayG1,pointDisplayG1Postion)
	surface.blit(pointDisplayG2,pointDisplayG2Postion)
