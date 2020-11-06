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


#Főcím:
print()
print("          Torpedó játék")
print()

#Táblázat:
table = [["   "," A "," B "," C "," D "," E "," F "," G "," H "," I "," J "],
[" 1 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 2 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 3 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 4 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 5 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 6 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 7 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 8 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" 9 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
["10 "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "]]

#Hajó típusok:
Carrier = int(5)
Battleship = int(4)
Cruiser = int(3)
Submarine = int(3)
Destroyer = int(2)

Ships = [Carrier, Battleship, Cruiser, Submarine, Destroyer]
shipNum = len(Ships)


#Táblázat rajzoló ciklusfüggvény:
def table_draw():
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

table_draw()

print("A fenti táblán 5db hadihajót kell elhelyezned. Ad meg a hajók helyzetét egyenként!")
print()
# Carrier = input("Add meg az 5 egység hosszú hordozó egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját (pl.: b1,b2): ")
# Battleship = input("Add meg az 4 egység hosszú csatahajó egyik végének kezdő koordinátájátv, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# Cruiser = input("Add meg az 3 egység hosszú cirkáló egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# Submarine = input("Add meg az 3 egység hosszú tengeralattjáró egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# Destroyer = input("Add meg az 2 egység hosszú romboló egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")

def randCoord():
    x = int(0)
    y = int(0)
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    return x, y

def randDir(coord,Shiptype):

    direction = []

    if coord[1] >= Shiptype:
        direction.append("left")

    if coord[1] <= 11-Shiptype:
        direction.append("right")

    if coord[0] >= Shiptype:
        direction.append("up")

    if coord[0] <= 11-Shiptype:
        direction.append("down")
    return(random.choice(direction))

def ship(coord,dir,Shiptype):
    table[coord[0]][coord[1]] = " H "
    if dir is "right":
        i = 0
        while i < Shiptype:
            while table[coord[0]][coord[1]+i] is not " H ":
                table[coord[0]][coord[1]+i] = " H "
            i += 1

    if dir is "left":
        i = 0
        while i < Shiptype:
            while table[coord[0]][coord[1]-i] is not " H ":
                table[coord[0]][coord[1]-i] = " H "
            i += 1

    if dir is "up":
        i = 0
        while i < Shiptype:
            while table[coord[0]-i][coord[1]] is not " H ":
                table[coord[0]-i][coord[1]] = " H "
            i += 1

    if dir is "down":
        i = 0
        while i < Shiptype:
            while table[coord[0]+i][coord[1]] is not " H ":
                table[coord[0]+i][coord[1]] = " H "
            i += 1

def randShips():
    coord = randCoord()
    for i in Ships:
        dir = randDir(coord,i)
        ship(coord,dir,i)
        while table[coord[0]][coord[1]] is " H ":
            coord = randCoord()
        i += 1


randShips()

table_draw()
