from ColorSet import *
FPS=60
OFFSET=20#spostamento in pixel del giocatore
MAXX,MAXY=1200,600#dimensioni della schermata di gioco
pointFontDim=30#dimensioni del font usato per stampare i punti
wclFontDim=36#dimensioni del font usato per stampare nella schermata di benveuto
#font usati
pointFont=None
wclFont=None
#dimensioni iniziali del giocatore
playerDimX=60
playerDimY=60

backgroundColor=BLACK#colore dell sfondo
playerPntStart=0#punti iniziali del giocatore
danno=10#danno che subisce il giocatore se prende il nemico con il colore sballato
#dimensioni delle immagne usata nello schermod el game over
gameOverX=420
gameOverY=281
new=500#tempo per generare un nuovo nemico
dimWarn=(playerDimX+playerDimY)/4#dimensione considerata pericolsa per il giocatore, al disotto di essa si puo' curare
cure=danno/2#cura
maxObs=20#numero ostacolo
#tasti del fuoco
fireUP="i"
fireDW="k"
fireDX="l"
fireSX="j"
numOfUsedColor=4
enemyDim=playerDimY/2#dimensione del nemico
obsColor=DARKGREEN