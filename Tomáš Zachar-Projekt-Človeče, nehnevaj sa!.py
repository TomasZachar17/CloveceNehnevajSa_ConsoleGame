"""
skript rieši všetky časti zadania projektu
po spustení si môže užívatel vybrať, či chce spustit simuláciu 1 hráča, alebo hru 2 hráčov

pohyb hráčov je spravený ako animácia pomocou knižníc time a os, pomocou ktorých vymazávam celý obsah terminálu a znova vykreslujem
plochu, už s figúrkou alebo figúrkami na iných pozíciach

simulácia 1 sa skončí, keď sa hráč dostane do domčeka, v zadaní bolo, že nech sa hráč dostane na jednu
z pozícii označených pismenom D, no môj hráč sa musí dostať presne na posledné políčko domčeka a musí na
konci hodiť presne také číslo, aby sa tam dostal

hra 2 hráčov funguje nasledovne:
program si vypíta velkosť plochy
plocha sa vykreslí a nasledovne každý hráč hodí kockou
začína hráč s väčším hodom, ak hodia rovnaké číslo hádžu ešte raz
potom sa hráči striedaju v hodoch kockou
ak hráč hodi číslo 6, objaví sa mu figúrka na začiatočnom políčku
hráč môže mať na ploche najviac (n-3/2) figúriek 
ak má hráč figúrky na ploche, program mu vypíše, že na akých X,Y sa nachádzaju jeho figúrky a môže si vybrať ktorou chce pohnúť
ak hráč prejde cez iného hráča, hráč cez ktorého bolo prejdené ostane na svojom mieste
ak hráč ukončí jeho ťah na figúrke druhého hráča, tá figúrka sa vymaže
ak hráč hodí také číslo že by jeho figúrka pristála na vlastnej, s tou figurkou nemôže pohnúť
hráč musí na konci hodiť presne také číslo aby sa dostal do posledného voľného miesta v domčeku
hra končí ak jeden z hráčov zaplní všetky miesta v domčeku
"""
import os,time,random,copy
os.system('cls')
os.system('color 7f')


def gensachovnicu(n):
    """
    Generuje a vráti hraciu plochu n x n
    """
    prvyriadok = []
    for i in range(n):
        if i>9:prvyriadok.append(i-(10*(i//10)))
        else:prvyriadok.append(i)
    hracia_plocha = [["0"]*n for _ in range(n)]
    X=int((n-1)/2)
    hracia_plocha[X][X]='X'
    hracia_plocha[X][n-1],hracia_plocha[n-1][X],hracia_plocha[X][0],hracia_plocha[0][X]='*','*','*','*'
    for i in range(1,int(((n-1)/2))):
        hracia_plocha[X-i][X],hracia_plocha[X][X-i],hracia_plocha[X+i][X],hracia_plocha[X][X+i]='D','D','D','D'
    for i in range(n):
        for j in range(n):
            if hracia_plocha[j][i]=='0':hracia_plocha[j][i]=' '
    for i in range(n):
        if i == X:continue
        hracia_plocha[i][X+1],hracia_plocha[i][X-1]='*','*'
    for i in range(n):
        if i == X:continue
        hracia_plocha[X+1][i],hracia_plocha[X-1][i]='*','*'
    hracia_plocha.insert(0,prvyriadok)
    nulty_riadok = list(hracia_plocha[0])
    nulty_riadok.insert(0," ")
    hracia_plocha[0]=nulty_riadok
    for i in range(n):
        Ity_riadok = list(hracia_plocha[i+1])
        if i > 9:Ity_riadok.insert(0,i-(10*(i//10))) 
        else:Ity_riadok.insert(0,i)
        hracia_plocha[i+1]=Ity_riadok
    return hracia_plocha


def tlacsachovnicu(sachovnica):
    """
    Vykreslí hraciu plochu vygenerovanú funkciou gensachovnicu
    """
    for i in sachovnica:
        for j in i:
            print(j,end="  ")
        print()


def pozicia_hraca(sachovnica,hrac):
    """
    Vráti X,Y figúrky na ploche , funguje len ak je na ploche len jeden hráč
    Použiva sa v simúlácii hry 1 hráča
    """
    for i in range(1,len(sachovnica)):
        for j in range(1,len(sachovnica)):
            if sachovnica[i][j]==hrac:HracX, HracY = j,i
    return HracX, HracY  


def pozicie_hracov(sachovnica):
    """
    Vráti X,Y figúriek na ploche, funguje ak je na ploche hocikolko figúriek
    Používa sa v hre 2 hráčov
    """
    pozicie_panakov_A=[]
    pozicie_panakov_B=[]
    for i in range(1,len(sachovnica)):
        for j in range(1,len(sachovnica)):
            if sachovnica[i][j]=='A':
                pozicie_panakov_A.extend([j - 1, i - 1])
            elif sachovnica[i][j]=='B':
                pozicie_panakov_B.extend([j - 1, i - 1])
    return [pozicie_panakov_A,pozicie_panakov_B]


def pozicia_stredu(sachovnica):
    """
    Vráti súradnice stredu hracej plochy
    """
    return len(sachovnica) // 2


def volne_miesto_v_domceku(sachovnica,hrac):
    """
    Vráti kolko je volného miesta v domčeku daného hráča
    """
    StredIndex = pozicia_stredu(sachovnica)
    max_miesta = (len(sachovnica) // 2) - 2
    volne_miesta = max_miesta
    posun = -1 if hrac == 'A' else 1
    for i in range(max_miesta):
        if sachovnica[StredIndex + (posun * (i + 1))][StredIndex] == hrac:
            volne_miesta = max_miesta - (i + 1)
        else:
            break
    return volne_miesta


def pocet_krokov_do_ciela(sachovnica,hrac,HracX,HracY):
    """
    Vráti kolko krokov musí ešte daná figúrka vykonať, aby sa dostala na políčko do domčeka, kam patrí
    """
    sachovnica_nova=gensachovnicu(len(sachovnica)-1)
    sachovnica_nova[HracY][HracX]=hrac
    StredIndex = pozicia_stredu(sachovnica_nova)
    i=0
    global hracia_plocha_kopia, volne_miesto_v_domceku_A, volne_miesto_v_domceku_B
    volne_miesto_v_domceku_A=volne_miesto_v_domceku(sachovnica,'A')
    volne_miesto_v_domceku_B=volne_miesto_v_domceku(sachovnica,'B')
    hracia_plocha_kopia=gensachovnicu(len(sachovnica_nova)-1)
    while sachovnica_nova[StredIndex-(int(len(sachovnica_nova)/2-2)-(volne_miesto_v_domceku_A if hrac=='A' else volne_miesto_v_domceku_B))+(-1 if hrac=='A' else +1)][StredIndex]!=hrac:
        sachovnica2=list(sachovnica_nova)
        HracX=pozicia_hraca(sachovnica2,hrac)[0]
        HracY=pozicia_hraca(sachovnica2,hrac)[1]
        sachovnica_nova=list(pohyb(sachovnica2,hrac,HracX,HracY))
        i+=1
    return i


def znak_policka_na_ktore_dopadnem_po_n_tahoch(sachovnica,HracX,HracY,hrac,n):
    """
    Vráti znak políčka na aké sa dostane figúrka po n krokoch

    Využíva sa na to, že keby sa figúrka dostala po hode kockou na políčko 
    s vlastným hráčom, táto figúrka nemôže vykonať tento ťah
    """
    global hracia_plocha_kopia
    hracia_plocha2=gensachovnicu(len(sachovnica)-1)
    hracia_plocha_kopia=gensachovnicu(len(sachovnica)-1)
    hracia_plocha2[HracY][HracX]=hrac
    for i in range(n):
        HracX=pozicia_hraca(hracia_plocha2,hrac)[0]
        HracY=pozicia_hraca(hracia_plocha2,hrac)[1]
        pohyb(hracia_plocha2,hrac,HracX,HracY)
    HracX=pozicia_hraca(hracia_plocha2,hrac)[0]
    HracY=pozicia_hraca(hracia_plocha2,hrac)[1]
    return sachovnica[HracY][HracX]


def pohyb(sachovnica,hrac,HracX,HracY):
    """
    Vráti hraciu plochu už s vykonaným 1 krokom daného hráča
    """
    global HracY_vybratej_figurky,HracX_vybratej_figurky,hracia_plocha_kopia
    StredIndex=pozicia_stredu(sachovnica)
    if HracY==1 and HracX==StredIndex and hrac=='A':sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX#VCHOD HRACA A DO DOMCEKA
    elif HracY==1 and HracX==StredIndex and hrac=='B':sachovnica[HracY][HracX],sachovnica[HracY][HracX+1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX+1
    elif HracX==StredIndex and HracY-StredIndex<-1:sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX
    elif HracY==len(sachovnica)-1 and HracX==StredIndex and hrac=='B':sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX#VCHOD HRACA B DO DOMCEKA
    elif HracY==len(sachovnica)-1 and HracX==StredIndex and hrac=='A':sachovnica[HracY][HracX],sachovnica[HracY][HracX-1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX-1
    elif HracX==StredIndex and HracY-StredIndex>1:sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX
    elif HracX-StredIndex==1 and HracY-StredIndex==-1:sachovnica[HracY][HracX],sachovnica[HracY][HracX+1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX+1#VNUTORNE ROHY
    elif HracX-StredIndex==-1 and HracY-StredIndex==1:sachovnica[HracY][HracX],sachovnica[HracY][HracX-1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX-1
    elif HracX-StredIndex==1 and HracY-StredIndex==1:sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX
    elif HracX-StredIndex==-1 and HracY-StredIndex==-1:sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX
    elif HracX==StredIndex and HracY==1:sachovnica[HracY][HracX],sachovnica[HracY][HracX+1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX+1#STREDY RAMIEN
    elif HracX==StredIndex and HracY==len(sachovnica)-1:sachovnica[HracY][HracX],sachovnica[HracY][HracX-1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX-1
    elif HracY==StredIndex and HracX==1:sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX
    elif HracY==StredIndex and HracX==len(sachovnica)-1:sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX
    elif HracX-StredIndex==1 and HracY-StredIndex<-1:sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX#POHYB V PRAVOM HORNOM KVADRANTE
    elif HracY-StredIndex==-1 and HracX-StredIndex>1 and HracX<len(sachovnica)-1:sachovnica[HracY][HracX],sachovnica[HracY][HracX+1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX+1
    elif HracY-StredIndex==-1 and HracX==len(sachovnica)-1:sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX
    elif HracY-StredIndex==1 and HracX-StredIndex>1:sachovnica[HracY][HracX],sachovnica[HracY][HracX-1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX-1#POHYB V PRAVOM DOLNOM KVADRANTE
    elif HracX-StredIndex==1 and HracY-StredIndex>1 and HracY<len(sachovnica)-1:sachovnica[HracY][HracX],sachovnica[HracY+1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY+1,HracX
    elif HracX-StredIndex==1 and HracY==len(sachovnica)-1:sachovnica[HracY][HracX],sachovnica[HracY][HracX-1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX-1
    elif HracX-StredIndex==-1 and HracY-StredIndex>1:sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX#POHYB V LAVOM DOLNOM KVADRANTE
    elif HracY-StredIndex==1 and HracX-StredIndex<-1 and HracX>1:sachovnica[HracY][HracX],sachovnica[HracY][HracX-1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX-1
    elif HracY-StredIndex==1 and HracX==1:sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX
    elif HracY-StredIndex==-1 and HracX-StredIndex<-1:sachovnica[HracY][HracX],sachovnica[HracY][HracX+1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX+1#POHYB V LAVOM HORNOM KVADRANTE
    elif HracX-StredIndex==-1 and HracY-StredIndex<-1 and HracY>1:sachovnica[HracY][HracX],sachovnica[HracY-1][HracX],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY-1,HracX
    elif HracX-StredIndex==-1 and HracY==1:sachovnica[HracY][HracX],sachovnica[HracY][HracX+1],HracY_vybratej_figurky,HracX_vybratej_figurky=hracia_plocha_kopia[HracY][HracX],hrac,HracY,HracX+1
    return sachovnica



def simulacia_jedneho_panacika():
    """
    Simulácia jedného hráča, na ploche je len 1 figúrka hráča A,
    hádže kockou a hýbe sa, kým sa nedostane na políčko D najbližšie k stredu
    """
    velkost = int(input("Zadaj veľkosť hracej plochy (neparne číslo) : "))
    while velkost%2==0 or velkost<3:
        velkost = int(input("!!!ZADAJ NEPÁRNE ČÍSLO VäČŠIE AKO 3!!! : "))
    os.system('cls')
    hrac='A'
    hracia_plocha = list(gensachovnicu(velkost))
    StredIndex=pozicia_stredu(hracia_plocha)
    hracia_plocha[1][StredIndex+1]=hrac
    tlacsachovnicu(hracia_plocha)
    hody_kockou=[]
    pocet_krokov_do_ciela_=None
    global volne_miesto_v_domceku_A,hracia_plocha_kopia
    volne_miesto_v_domceku_A = volne_miesto_v_domceku(hracia_plocha,hrac)
    while pocet_krokov_do_ciela_!=0:
        os.system('cls')
        tlacsachovnicu(hracia_plocha)
        hod_kockou = random.randint(1,6)
        hody_kockou.append(hod_kockou)
        print("Hody kockou : ",hody_kockou)
        hracia_plocha2=copy.deepcopy(hracia_plocha)
        HracX=pozicia_hraca(hracia_plocha2,hrac)[0]
        HracY=pozicia_hraca(hracia_plocha2,hrac)[1]
        pocet_krokov_do_ciela_=pocet_krokov_do_ciela(hracia_plocha2,hrac,HracX,HracY)
        print("Počet krokov do cieľa : ",pocet_krokov_do_ciela_)
        if hod_kockou>pocet_krokov_do_ciela_:#Hráč musí na konci hodiť také číslo aby sa presne dostal na políčko D najbližšie k stredu
            print("Hráč hádže znova lebo hodil viac ako je krokov do ciela")
            time.sleep(2)
        else:
            time.sleep(2)
            hracia_plocha_kopia=gensachovnicu(len(hracia_plocha)-1)
            for i in range(hod_kockou):
                time.sleep(0.1)
                os.system('cls')
                HracX=pozicia_hraca(hracia_plocha,hrac)[0]
                HracY=pozicia_hraca(hracia_plocha,hrac)[1]
                tlacsachovnicu(list(pohyb(hracia_plocha,hrac,HracX,HracY)))
                print("Hody kockou : ",hody_kockou)
                hracia_plocha2=copy.deepcopy(hracia_plocha)
                HracX=pozicia_hraca(hracia_plocha2,hrac)[0]
                HracY=pozicia_hraca(hracia_plocha2,hrac)[1]
                pocet_krokov_do_ciela_=pocet_krokov_do_ciela(hracia_plocha2,hrac,HracX,HracY)
                print("Počet krokov do cieľa : ",pocet_krokov_do_ciela_)
    input("Stlač ENTER pre návrat do menu")


def hra_2_hracov():
    """
    Hra 2 hráčov
    (detailný opis na riadkoch 12-24)
    """
    velkost = int(input("Zadaj veľkosť hracej plochy (neparne číslo) : "))
    while velkost%2==0 or velkost<4:
        velkost = int(input("!!!ZADAJ NEPÁRNE ČÍSLO VäČŠIE AKO 3!!! : "))
    os.system('cls')
    hracia_plocha = list(gensachovnicu(velkost))
    tlacsachovnicu(hracia_plocha)
    global hody_hraca_A,hody_hraca_B
    hody_hraca_A,hody_hraca_B=[],[]
    hod_kockou_A,hod_kockou_B=0,0
    while hod_kockou_B==hod_kockou_A:#Hráči hádžu kockou, aby sa rozhodlo kto začne prvý, ten kto hodil väčšie číslo ide prvý
        hod_kockou_A = random.randint(1,6)
        hod_kockou_B = random.randint(1,6)
        print("Hráč A hodil číslo : ",hod_kockou_A)
        print("Hráč B hodil číslo : ",hod_kockou_B)
        if hod_kockou_A > hod_kockou_B:hrac_na_rade='A'
        elif hod_kockou_A < hod_kockou_B:hrac_na_rade='B'
        else: print("Hráči hodili rovnaké čísla hádže sa ešte raz")
        if hod_kockou_A != hod_kockou_B:print("Začína hráč ",hrac_na_rade)
    input("Stlač ENTER pre začiatok hry")
    global HracX_vybratej_figurky, HracY_vybratej_figurky, hracia_plocha_kopia, volne_miesto_v_domceku_A,volne_miesto_v_domceku_B
    volne_miesto_v_domceku_A,volne_miesto_v_domceku_B = volne_miesto_v_domceku(hracia_plocha,'A'),volne_miesto_v_domceku(hracia_plocha,'B')
    hra=True
    StredIndex=pozicia_stredu(hracia_plocha)
    while hra==True:#Hlavný cyklus ktorý beží až kým jeden z hráčov nevyhrá
        vyber_figurky_na_pohyb=0
        counter_pohybu=0
        if hrac_na_rade == 'A':#Hodu kockou hráča A a zápis toho hodu do listu so všetkými hodmi hráča A
            hod_kockou = random.randint(1,6)
            hody_hraca_A.append(hod_kockou)
            if hod_kockou==6 and hracia_plocha[1][StredIndex+1]!=hrac_na_rade and len(pozicie_hracov(hracia_plocha)[0])/2<(velkost-3)/2:hracia_plocha[1][StredIndex+1]=hrac_na_rade
            else:counter_pohybu+=hod_kockou
        else:#Hodu kockou hráča B a zápis toho hodu do listu so všetkými hodmi hráča B
            hod_kockou = random.randint(1,6)
            hody_hraca_B.append(hod_kockou)
            if hod_kockou==6 and hracia_plocha[len(hracia_plocha)-1][StredIndex-1]!=hrac_na_rade and len(pozicie_hracov(hracia_plocha)[1])/2<(velkost-3)/2:hracia_plocha[len(hracia_plocha)-1][StredIndex-1]=hrac_na_rade
            else:counter_pohybu+=hod_kockou
        while hod_kockou == 6:#Ak hráč hodí 6, hádže ešte raz
            if hrac_na_rade == 'A':
                hod_kockou = random.randint(1,6)
                hody_hraca_A.append(hod_kockou)
                if hod_kockou==6 and hracia_plocha[1][StredIndex+1]!=hrac_na_rade and len(pozicie_hracov(hracia_plocha)[0])/2<(velkost-3)/2:hracia_plocha[1][StredIndex+1]=hrac_na_rade
                else:counter_pohybu+=hod_kockou
            else:
                hod_kockou = random.randint(1,6)
                hody_hraca_B.append(hod_kockou)
                if hod_kockou==6 and hracia_plocha[len(hracia_plocha)-1][StredIndex-1]!=hrac_na_rade and len(pozicie_hracov(hracia_plocha)[1])/2<(velkost-3)/2:hracia_plocha[len(hracia_plocha)-1][StredIndex-1]=hrac_na_rade
                else:counter_pohybu+=hod_kockou
        os.system('cls')
        tlacsachovnicu(hracia_plocha)
        print("Všetky hody hráča A : ",hody_hraca_A)
        print("Všetky hody hráča B : ",hody_hraca_B)
        print("Na rade je hráč",hrac_na_rade,"a hodil :",counter_pohybu,", môže pohnúť týmito figúrkami :")
        if hrac_na_rade=='A':#Výber figúrky na pohyb hráča A
            figurky_s_nepovolenymi_tahmi=[]
            if len(pozicie_hracov(hracia_plocha)[0])<1:print("Nemáš ešte figúrky na ploche, figúrka sa ti objaví keď hodíš 6, stlač ENTER pre hru ďalej."),input()#Toto sa vykoná ak hráč A nemá žiadnu figúrku na ploche
            else:
                counter=0#Počítadlo(s kolkými hráčmi je možný ťah)
                for i in range(int(len(list(pozicie_hracov(hracia_plocha)[0]))/2)):#Vípis všetkých figúriek hráča A a ich X,Y a či je možný ťah s určitou figúrkou
                    if pocet_krokov_do_ciela(hracia_plocha,hrac_na_rade,pozicie_hracov(hracia_plocha)[0][i*2]+1,pozicie_hracov(hracia_plocha)[0][i*2+1]+1)>=counter_pohybu and znak_policka_na_ktore_dopadnem_po_n_tahoch(hracia_plocha,pozicie_hracov(hracia_plocha)[0][i*2]+1,pozicie_hracov(hracia_plocha)[0][i*2+1]+1,hrac_na_rade,hod_kockou)!=hrac_na_rade: 
                        print("Figúrka",i+1,"--> ",end="")
                        for j in range(2):
                            if j==0:print("X: ",end="")
                            else:print("Y: ",end="")
                            print(list(pozicie_hracov(hracia_plocha))[0][j+(i*2)],end=" ")
                        print()
                        counter+=1
                    else: figurky_s_nepovolenymi_tahmi.append(i+1),print("Figúrkou",i+1,"nemôžeš pohnúť")
                if counter != 0:#Výber figúrky, s ktorou sa chce hráč pohnúť, ak je aspoň s jednou možný ťah
                    vyber_figurky_na_pohyb=int(input("Ktorou figúrkou chceš pohnúť? :"))
                    while 1>vyber_figurky_na_pohyb or vyber_figurky_na_pohyb>len(list(pozicie_hracov(hracia_plocha)[0]))/2 or vyber_figurky_na_pohyb in figurky_s_nepovolenymi_tahmi:
                        if vyber_figurky_na_pohyb in figurky_s_nepovolenymi_tahmi:
                            print("Tou figúrkou nemôžeš pohnúť, zadaj nové číslo: ",end="")
                            vyber_figurky_na_pohyb=int(input())
                        else:
                            print("Zadaj číslo od :",1,"do :",counter,": ",end="")
                            vyber_figurky_na_pohyb=int(input())
                else:print("Nemáš žiadnu figúrku s ktorou môžeš pohnúť, stlač ENTER pre pokračovanie hry."),input()#Toto sa vykoná ak so žiadnou figúrkou nieje možný ťah
        else:#Výber figúrky na pohyb hráča B
            figurky_s_nepovolenymi_tahmi=[]
            if len(pozicie_hracov(hracia_plocha)[1])/2<1:print("Nemáš ešte figúrky na ploche, figúrka sa ti objaví keď hodíš 6, stlač ENTER pre hru ďalej."),input()#Toto sa vykoná ak hráč B nemá žiadnu figúrku na ploche
            else:
                counter=0#Počítadlo(s kolkými hráčmi je možný ťah)
                for i in range(int(len(list(pozicie_hracov(hracia_plocha)[1]))/2)):#Vípis všetkých figúriek hráča B a ich X,Y a či je možný ťah s určitou figúrkou
                    if pocet_krokov_do_ciela(hracia_plocha,hrac_na_rade,pozicie_hracov(hracia_plocha)[1][i*2]+1,pozicie_hracov(hracia_plocha)[1][i*2+1]+1)>=counter_pohybu and znak_policka_na_ktore_dopadnem_po_n_tahoch(hracia_plocha,pozicie_hracov(hracia_plocha)[1][i*2]+1,pozicie_hracov(hracia_plocha)[1][i*2+1]+1,hrac_na_rade,hod_kockou)!=hrac_na_rade:
                        print("Figúrka",i+1,"--> ",end="")
                        for j in range(2):
                            if j==0:print("X: ",end="")
                            else:print("Y: ",end="")
                            print(list(pozicie_hracov(hracia_plocha))[1][j+(i*2)],end=" ")   
                        print()
                        counter+=1
                    else: figurky_s_nepovolenymi_tahmi.append(i+1),print("Figúrkou",i+1,"nemôžeš pohnúť")
                if counter != 0:#Výber figúrky, s ktorou sa chce hráč pohnúť, ak je aspoň s jednou možný ťah
                    vyber_figurky_na_pohyb=int(input("Ktorou figúrkou chceš pohnúť? :"))
                    while 1>vyber_figurky_na_pohyb or vyber_figurky_na_pohyb>len(list(pozicie_hracov(hracia_plocha)[1]))/2 or vyber_figurky_na_pohyb in figurky_s_nepovolenymi_tahmi:
                        if vyber_figurky_na_pohyb in figurky_s_nepovolenymi_tahmi:
                            print("Tou figúrkou nemôžeš pohnúť, zadaj nové číslo: ",end="")
                            vyber_figurky_na_pohyb=int(input())
                        else:
                            print("Zadaj číslo od :",1,"do :",counter,": ",end="")
                            vyber_figurky_na_pohyb=int(input())
                else:print("Nemáš žiadnu figúrku s ktorou môžeš pohnúť, stlač ENTER pre pokračovanie hry."),input()#Toto sa vykoná ak so žiadnou figúrkou nieje možný ťah
        if hrac_na_rade=='A' and vyber_figurky_na_pohyb!=0:#Pohyb hráča A vybratou figúrkou
            HracX_vybratej_figurky = pozicie_hracov(hracia_plocha)[0][vyber_figurky_na_pohyb*2-2]+1
            HracY_vybratej_figurky = pozicie_hracov(hracia_plocha)[0][vyber_figurky_na_pohyb*2-1]+1
            hracia_plocha_kopia=copy.deepcopy(hracia_plocha)
            pomocna_plocha=gensachovnicu(len(hracia_plocha)-1)
            hracia_plocha_kopia[HracY_vybratej_figurky][HracX_vybratej_figurky]=pomocna_plocha[HracY_vybratej_figurky][HracX_vybratej_figurky]
            for i in range(counter_pohybu):
                time.sleep(0.1)
                os.system('cls')
                tlacsachovnicu((pohyb(hracia_plocha,hrac_na_rade,HracX_vybratej_figurky,HracY_vybratej_figurky)))
                print("Všetky hody hráča A : ",hody_hraca_A)
                print("Všetky hody hráča B : ",hody_hraca_B)
        elif hrac_na_rade=='B' and vyber_figurky_na_pohyb!=0:#Pohyb hráča B vybratou figúrkou
            HracX_vybratej_figurky = pozicie_hracov(hracia_plocha)[1][vyber_figurky_na_pohyb*2-2]+1
            HracY_vybratej_figurky = pozicie_hracov(hracia_plocha)[1][vyber_figurky_na_pohyb*2-1]+1
            hracia_plocha_kopia=copy.deepcopy(hracia_plocha)
            pomocna_plocha=gensachovnicu(len(hracia_plocha)-1)
            hracia_plocha_kopia[HracY_vybratej_figurky][HracX_vybratej_figurky]=pomocna_plocha[HracY_vybratej_figurky][HracX_vybratej_figurky]
            for i in range(counter_pohybu):
                time.sleep(0.1)
                os.system('cls')
                tlacsachovnicu((pohyb(hracia_plocha,hrac_na_rade,HracX_vybratej_figurky,HracY_vybratej_figurky)))
                print("Všetky hody hráča A : ",hody_hraca_A)
                print("Všetky hody hráča B : ",hody_hraca_B)
        if volne_miesto_v_domceku(hracia_plocha,hrac_na_rade)==0:hra=False,print("!!!VYHRAL HRÁČ",hrac_na_rade,"!!!")#Skúška, či niektorý z hráčov hráč po dokončení ťahu vyhral
        if hrac_na_rade=='A':hrac_na_rade='B'
        else:hrac_na_rade='A'
    input("Stlač ENTER pre návrat do menu")


while True:
    os.system('cls')
    print("Stlač 1. pre SIMULÁCIU JEDNÉHO HRÁČA")
    print("Stlač 2. pre HRU 2 HRÁČOV")
    vyber=0
    while vyber<1 or vyber>2:#Výber či chce užívatel spustit simuláciu 1 hráča či hru 2 hráčov
        try:
            vyber = int(input())
            if vyber==1:simulacia_jedneho_panacika()
            elif vyber==2:hra_2_hracov() 
            print("Zadaj jedno z čísel 1,2 :")
        except ValueError:
            print("Zadaj jedno z čísel 1,2 :")