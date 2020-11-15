# pylint: disable=unused-variable

# 5 hajó: 5e-1db; 4e:1db; 3e:2db; 2e:1db
# A-J; 1-10 tábla
# A hajók csak függőlegesen vagy vízszintesen lehetnek elrendezve, em lóghatnak ki, és nem lóghatnak egymásra
# Találat: X
# Nem talált: O
# Ha egy hajó minden elemét találat éri akkor az  elsüllyed, ezt jelezni kell.
# Játékosok feladata 1.: elhelyezni a hajókat a táblán a szabályoknak megfelelően
# Játékosok feladata 2.: lőni, úgy hogy minél nagyobb valószínűséggel találja el az ellenséget
# Játékosok feladata 3.: jelezni hogy talált vagy nem, illetve hogy elsűjedt-e a hajó, vagy hogy esűllyedt-e a flotta
# Játékosok feladata 4.: rögzíteni a próbálkozásokat és a találatokat


# Változók: üres táblázat; hajók, lövések, felhasználó neve.

# Kirajzoljuk a táblát, felette főcím.
# Üdvözöljük a felhasználót. Ismertetjük a játékszabályt.
# Hajók elhelyezése: megadjuk a hajók típusát, majd bekérjük a pozícióját egyesével, egy kezdőértéket és egy irányt. 
# A program kiegészíti a hajókat, és ellenőrizi hogy, nincs-e ütközés egy korábban elhelyezett hajóval, illetve nem lóg-e ki a táblázatból. 
# A számítógép randomgenerátort használ z elhelyezésre.
# Elekzdődnek a lövések a koordináták megadásával. A számítógép randomgenerátort használ először a teljes táblára, de ha talál akkor lecsöken a random scope-ja a környező koordinátákra, ha ismét talál akkor csak az adott vonal mentén lő. Ha az egyik irány elfogyott, akkor a másik irányt erőlteti.
# Ha elsűjed egy hajó akkor azt bejelentjük, a számítógép algoritmusa újból a tágab scope-on van.
# Ha az összes ellenséges hajó elsűjedt akkor bejelentjük a győzelmet, és megmutatjuk mindkét táblát.

import random
import os
import msvcrt

#Táblázat:
table = [["   "," A "," B "," C "," D "," E "," F "," G "," H "," I "," J "],
[" 0 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 1 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 2 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 3 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 4 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 5 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 6 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 7 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 8 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 9 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "]]

tableAirBomb = [["   "," A "," B "," C "," D "," E "," F "," G "," H "," I "," J "],
[" 0 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 1 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 2 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 3 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 4 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 5 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 6 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 7 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 8 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 9 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "]]

#Hajó típusok, a számértékük a hossukat jelöli:
CARRIER = 5
BATTLESHIP = 4
CRUISER = 3
SUBMARINE = 3
DESTROYER = 2

SHIPS = [CARRIER, BATTLESHIP, CRUISER, SUBMARINE, DESTROYER]
SHIPFLOTTLENGTH = len(SHIPS)
ALLRANDOMSHIPSCOORD = []
SHINKSHIPCOUNT = 0
AIRBOMBLEFT = 17


#Táblázat rajzoló ciklusfüggvény:
def table_draw(table):
    # os.system('cls')
    print()
    print("          Torpedó játék")
    print()
    row = int(0)
    col = int(0)
    for i in table[row]:
        for i in table:
            print(table[row][col], end="")
            col += 1     
        col = 0
        row += 1
        print()
    print()

table_draw(table)

#print("A fenti táblán 5db hadihajót kell elhelyezned. Ad meg a hajók helyzetét egyenként!")
#print()
# CARRIER = input("Add meg az 5 egység hosszú hordozó egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját (pl.: b1,b2): ")
# BATTLESHIP = input("Add meg az 4 egység hosszú csatahajó egyik végének kezdő koordinátájátv, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# CRUISER = input("Add meg az 3 egység hosszú cirkáló egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# SUBMARINE = input("Add meg az 3 egység hosszú tengeralattjáró egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# DESTROYER = input("Add meg az 2 egység hosszú romboló egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")


# def randDir(shipLength):

direction = []
dircoord = [0,0]
x = random.randint(1, 10)
y = random.randint(1, 10)
a = 0
coord = [x,y]
print("x,y random coordináták:",coord)
table[coord[0]][coord[1]] = " H "
shipLength = SHIPS[a]
while a < SHIPFLOTTLENGTH:
    a += 1
print("random coordináták:",x,y)
if y >= shipLength:
    dircoord = dircoord[0]+1,dircoord[1]
    print("jobb",dircoord)
    direction.append(dircoord)
    dircoord = dircoord[0]-1,dircoord[1]
if y <= 11-shipLength:
    dircoord = dircoord[0]-1,dircoord[1]
    print("bal",dircoord)
    direction.append(dircoord)
    dircoord = dircoord[0]+1,dircoord[1]
if x >= shipLength:
    dircoord = dircoord[0],dircoord[1]+1
    print("fel",dircoord)
    direction.append(dircoord)
    dircoord = dircoord[0],dircoord[1]-1
if x <= 11-shipLength:
    dircoord = dircoord[0],dircoord[1]-1
    print("le",dircoord)
    direction.append(dircoord)
    dircoord = dircoord[0],dircoord[1]+1
print("lehetséges irányok:",direction)
print("random irány:",random.choice(direction))

def ship(shipLength):
    #table[coord[0]][coord[1]] = " H "
    dir = randDir(coord,shipLength)
    print("rdir:",dir)
    print("Yo")
    print("hajó hossz:",shipLength)
    allSHIPSCoord = []
    shipCoord = [coord[0] + dir[0]][coord[1] + dir[1]]
    print(shipCoord)
    allSHIPSCoord.append(shipCoord)
    i = 0
    while i < shipLength:
        if table[shipCoord[0]][shipCoord[1]] != " H ":
            i += 1
            print("Van hely?:",i)
        else:
            i = 0
            coord = randCoord()
            shipCoord = dir[0],dir[1]
            dir = randDir(coord,shipLength)
            print("Újragenerálás!")
        i = 0
        while i <= shipLength:
            print("Yoo")
            table[dir[0]][dir[1]] = " H "
            shipCoord = dir[0],dir[1]
            allSHIPSCoord.append(shipCoord)
            i += 1 
    return allSHIPSCoord   

def randSHIPS():
    global ALLRANDOMSHIPSCOORD
    a = 0
    while a < SHIPFLOTTLENGTH:
        allSHIPSCoord = []
        allSHIPSCoord = ship(SHIPS[a])
        ALLRANDOMSHIPSCOORD.append(allSHIPSCoord)
        print("Leraktam a hajót!")
        print("a értéke(max. a hajók száma.):",a)
        a += 1
    return ALLRANDOMSHIPSCOORD

def inputCoord():
    char = " abcdefghijq"
    char1 = " 0123456789q"
    coordStr1 = "_"
    coordStr2 = "_"
    coord = [int(-1),int(-1)]
    while coord[0] == -1 and coord[0] != 11:
        print("Adj meg egy értéket a vízszintes tengelyen a-j-ig:")
        coordStr1 = msvcrt.getwch()
        print("A koordináta:",coordStr1,",",coordStr2)
        coordStr1.casefold()
        coord[0] = char.find(coordStr1[0],1,12)
    while coord[1] == -1 and coord[0] != 11:
        print("Adj meg egy értéket a függőleges tengelyen 0-9-ig:")
        coordStr2 = msvcrt.getwch()
        print("A koordináta:",coordStr1,",",coordStr2)
        coordStr2.casefold()
        coord[1] = char1.find(coordStr2[0],1,12)
    return coord

def sink(Air_y,Air_x):
    AirY = int(0)
    AirX = int(0)
    s = []
    shipPart = []
    global SHINKSHIPCOUNT
    for i in range(0,11):
        for k in range(0,11):
            if tableAirBomb[AirX][AirY] == " T ":
                s = (AirX,AirY)
                shipPart.append(s)
            AirX += 1     
        AirX = 0
        AirY += 1
    for i in ALLRANDOMSHIPSCOORD:
        if sorted(tuple(i)) == sorted(tuple(shipPart)):
            SHINKSHIPCOUNT += 1
            for i in shipPart:
                tableAirBomb[i[0]][i[1]] = " S "
                table[i[0]][i[1]] = " S "

def AirBombGame():
    global airBomb
    print("A számítógép elhelyezte az öt hajóból álló flottát, kezdődhet a játék!" )
    print()
    print("q = Kilépés")
    print()
    print("A légitámadásból", airBomb-1, "bombád maradt.")
    coord = [0,0]
    AirY = 0
    AirX = 0
    i = 0
    while i <= airBomb-1:
        if table[AirX][AirY] == " H ":
            table[AirX][AirY] = " T "
            tableAirBomb[AirX][AirY] = " T "
            sink(AirY,AirX)
            table_draw(tableAirBomb)
            print("Talált!")
            print()
            print("q = Kilépés")
            print()
            print("A légitámadásból", airBomb-i, "bombád maradt.")
        elif tableAirBomb[AirX][AirY] == " O " or tableAirBomb[AirX][AirY] == " T ":
            print("Ide már lőttél!")
            print()
            print("q = Kilépés")
            print()
            print("A légitámadásból", airBomb-i, "bombád maradt. Ne pazarolj!")
        elif table[AirX][AirY] == " _ ": 
            table[AirX][AirY] = " O "
            tableAirBomb[AirX][AirY] = " O "
            table_draw(tableAirBomb)
            print("Mellé...")
            print()
            print("q = Kilépés")
            print()
            print("A légitámadásból", airBomb-i, "bombád maradt.")
        coord = inputCoord()
        AirY = coord[0]
        AirX = coord[1]
        table_draw(tableAirBomb)
        if AirY == 11 or AirX == 11:
            print("Kilépés..")
            break
        i += 1
        

# randSHIPS()

# AirBombGame()

table_draw(table)

if SHINKSHIPCOUNT > 0:
    print("Gratulálunk!", SHINKSHIPCOUNT, "hajót sűlyeszetél el a flottából!")
else:
    print("Legközelebbre több szerencsét kívánunk...")
print()
print("Viszlát!")

# Extra funkciók:
# Megoldás oop -vel hajó öntőforma irányokkal stb.
# webes verzió elkészítése

# Tervezett funkciók:
# Játktípus választás, légitámadás, vagy hajócsata! Játék ismétlése, menü...

# Hibajavítás:
# nem tökéletes az elkerülő algoritmus? Lehetne plusz egy karakter távolság a hajók között. (ritkán egyes hajók 1 egységgel rövidebbek!, talána legkisebbel van a baj...) Ilyenkor a sink sem működik..

# Dokumentáció:
# kommentelni a részeket, áttekinthetővé tenni a kódot.
# Mi okozott nehézséget: komplex bemeneti szűrő észítése, funkciók egymásba ágyazása, loopok egymásba ágyazása, műveleti sorrend
