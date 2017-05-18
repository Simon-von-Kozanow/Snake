import pygame, random, sys,time
pygame.init()

print ("gra wlaczy sie za chwilke :)")
#importujemy muzyke 
try:
    sound = pygame.mixer.Sound("Soundtrack.ogg")
    print ("1")
except:
    try:
        sound = pygame.mixer.Sound("Soundtrack2.ogg")
        print ("2")
    except:
        pass
    

#ustalamy rozmiar okna.
szerokosc = 500
wysokosc = 500
#rozmiar kratki
kratka = 20
#obliczamy rozmiar okna, ale nie w pikselach lecz w ilosci kratek
szerokosc_pola = int(szerokosc / kratka)
wysokosc_pola = int(wysokosc/ kratka)
gameIcon = pygame.image.load('SnkLOGO.png')
pygame.display.set_icon(gameIcon)

#Ustalamy wartosci RGB kolorow
BIALY     = (255, 255, 255)
CZARNY     = (  0,   0,   0)   
CZERWONY       = (220,   0,   0)
FIOLET2     = (147, 112, 219)
ZOLTY = (255, 255, 0)
SZARY  = ( 30,  30,  30)
TLO_KOLOR = CZARNY

 
glowa = 0

#glowna funkcja calego programu. Jedyna jaka wlanczamy i caly program dziala :)
def main():
    global back, jabl, licznik_fps, plansza, czcionka
    licznik_fps = pygame.time.Clock()
    
    #inicjujemy okno
    plansza = pygame.display.set_mode((szerokosc, wysokosc))
    
    #importujemy obrazy
    back = pygame.image.load("snakeaq.jpg").convert()
    jabl = pygame.image.load("jablko.png").convert()
    
    plansza.blit(back,[60,0])
    
    czcionka = pygame.font.SysFont("Comic Sans MS", 18)
    pygame.display.set_caption("Nacisnij 'e'(latwy) lub 'm'(sredni) lub 'h'(trudny)")
 
    ekran_startowy()
    while True:
            GRA()
            gameover_screen()
def ekran_startowy():
    czcionka_start = pygame.font.SysFont("Comic Sans MS", 100)
    start_napis = czcionka_start.render("SNAKE!", True, CZERWONY)
    while True:
        back.blit(plansza,[0,0])
        plansza.blit(start_napis, [60,wysokosc/2-80])
        #menu_poczatkowe
        
        press_key = czcionka.render('Wybierz tryb trudnosci(patrz naglowek)', True,CZERWONY)
        plansza.blit(press_key, [szerokosc/4-30, wysokosc - 30])

        if SprCzyKlawisz():
            global FPS
            if tryb == "midle":
                FPS = 10
            elif tryb == "easy":
                FPS = 7
            elif tryb == "hard":
                FPS = 15
            elif tryb == "imp":
                FPS = 999999999
            break
        pygame.display.update() 
def gameover_screen():
    czcionka2 = pygame.font.SysFont('JOKERMAN', 120)
    game = czcionka2.render('Game', True, FIOLET2)
    over = czcionka2.render('Over', True, FIOLET2)
    gx = 0
    gy = 10
    ox = 0
    oy = 100
    done = False
    while not done:
        plansza.blit(game, [gx,gy])
        plansza.blit(over,[ox,oy])
        pygame.display.update()
        pygame.display.set_caption("GAME OVER -> aby kontynuowac nacisnij przycisk")
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                done = True
            
            
            
        
    main()

def SprCzyKlawisz():
    tf = False
    if len(pygame.event.get(pygame.QUIT)) > 0:
        zatrzymanie_gry()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            global tryb
            if e.key== pygame.K_ESCAPE:
                zatrzymanie_gry()
            elif e.key == pygame.K_e:
                tryb = "easy"
                return True
            elif e.key == pygame.K_h:
               tryb = "hard"
               return True
            elif e.key == pygame.K_m:
                tryb = "midle"
                return True
            elif e.key == pygame.K_i:
                tryb = "imp"
                return True
            
def zatrzymanie_gry():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
def siatka():
    for x in range(0, szerokosc, kratka): 
        pygame.draw.line(plansza, SZARY, (x, 0), (x, wysokosc))
    for y in range(0, wysokosc, kratka): 
        pygame.draw.line(plansza, SZARY, (0, y), (szerokosc, y))
def losowanie_miejsca():
    return {'x': random.randint(0, szerokosc_pola - 1), 'y': random.randint(0, wysokosc_pola - 1)}
     
def drawjedzonko(wspolrzedne):
    x = wspolrzedne['x'] * kratka
    y = wspolrzedne['y'] * kratka
    plansza.blit(jabl,[x,y])
def drawsnake(snake_xy):
    for wspolrzedne in snake_xy:
        x = wspolrzedne['x'] * kratka
        y = wspolrzedne['y'] * kratka
        snake_body = pygame.Rect(x, y, kratka, kratka)
        pygame.draw.rect(plansza, BIALY, snake_body)
 
        snake_head = pygame.Rect(snake_xy[glowa]['x']*kratka,snake_xy[glowa]['y']*kratka, kratka, kratka)
        pygame.draw.rect(plansza, FIOLET2, snake_head)
        
def drawwynik(wynik):
    wynik_napis = czcionka.render('WYNIK: %s' % (wynik), True, BIALY)
    wynik_pole = wynik_napis.get_rect()
    wynik_pole.topleft = (szerokosc - 100, 5)
    plansza.blit(wynik_napis, wynik_pole)
def napis_pauza():
    ft = pygame.font.SysFont("Comic Sans MS", 70)
    pauza_key = ft.render('PAUZA', True, ZOLTY)
    plansza.blit(pauza_key,[60,60] )
def GRA(): #w tej funkcji jest zamieszczony kod calej rozgrywka
    #ustawiamy nagłowek
    pygame.display.set_caption("sterowanie -> strzalki ; pauza -> spacja")
    start_x = random.randint(5, szerokosc_pola - 6)
    start_y = random.randint(5, wysokosc_pola - 6)
    
    #lista ze slownikami z elementami wenza i ich wspolrzednymi
    snake_xy = [{'x': start_x,     'y': start_y},
                  {'x': start_x - 1, 'y': start_y},
                  {'x': start_x - 2, 'y': start_y}]
    
    kierunek = "RIGHT" 
 
    jedzonko = losowanie_miejsca()
    # GLOWNA PETLA GRY. TAKA GLOWNA GLOWNA.
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                zatrzymanie_gry()
            elif event.type == pygame.KEYDOWN: 
                if (event.key == pygame.K_LEFT ) and kierunek != "RIGHT": #w jakim kierunku??
                    kierunek = "LEFT"
                elif (event.key == pygame.K_RIGHT ) and kierunek != "LEFT": #w jakim kierunku??
                    kierunek = "RIGHT"
                elif (event.key == pygame.K_UP ) and kierunek != "DOWN": #w jakim kierunku??
                    kierunek = "UP"
                elif (event.key == pygame.K_DOWN ) and kierunek != "UP": #w jakim kierunku??
                    kierunek = "DOWN"
                elif event.key == pygame.K_ESCAPE:#czy wylaczyc gre?
                    zatrzymanie_gry()
                if event.key == pygame.K_SPACE:# czy pauza??
                    napis_pauza()
                    while True: 
                        napis_pauza()
                        pygame.display.update()
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            zatrzymanie_gry()
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            zatrzymanie_gry()
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                            break
 
        #czy nie dotyka brzegu ekranu??
        if snake_xy[glowa]['x'] == -1 or snake_xy[glowa]['x'] == szerokosc_pola or snake_xy[glowa]['y'] == -1 or snake_xy[glowa]['y'] == wysokosc_pola:
            gameover_screen()
        #czy nie dotyka glowa siebie samego?
        for snake_body in snake_xy[1:]:
            if snake_body['x'] == snake_xy[glowa]['x'] and snake_body['y'] == snake_xy[glowa]['y']:
                gameover_screen() 
 
        #czy zjadl jablko?
        if snake_xy[glowa]['x'] == jedzonko['x'] and snake_xy[glowa]['y'] == jedzonko['y']:
            print (" MNIAM... MNIAM... MNIAM .........")
            jedzonko = losowanie_miejsca() 
        else: #  DO WYTLUMACENIA!!  => jezeli zjadl to oznacza ze nie wydluza sie a jak zjadl to sie wydluza.
            del snake_xy[-1]
 
        
        if kierunek == "UP":
            nowaglowa = {'x': snake_xy[glowa]['x'], 'y': snake_xy[glowa]['y'] - 1}
        elif kierunek == "DOWN":
            nowaglowa = {'x': snake_xy[glowa]['x'], 'y': snake_xy[glowa]['y'] + 1}
        elif kierunek == "LEFT":
            nowaglowa = {'x': snake_xy[glowa]['x'] - 1, 'y': snake_xy[glowa]['y']}
        elif kierunek == "RIGHT":
            nowaglowa = {'x': snake_xy[glowa]['x'] + 1, 'y': snake_xy[glowa]['y']}

        snake_xy.insert(0, nowaglowa)

        
        plansza.fill(TLO_KOLOR)
        siatka()
        drawsnake(snake_xy)
        drawjedzonko(jedzonko)
        drawwynik(len(snake_xy) - 3)
        pygame.display.update()
        licznik_fps.tick(FPS)


sound.play()
main()

