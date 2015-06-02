###############################################################################
###############################################################################
# Very simple test implementation of a basic rougelike, just for the giggles
# and to see where the "real work" in such a thing is
# Author: Skeldir
# Date of Creation: 06.20.12
#
#
# No/hardly any comments, because it wouldn't make sense for just a small file
# besides, it is mostly self-explanatory 
###############################################################################
###############################################################################
import random
random.seed("somerandomseedstringthing")
global d
global p
###############################################################################
# the dungeon
class dungeon(object):
  def __init__(self):
    self.width=20
    self.height=20
    self.tiles={}
    for x in range(0,self.width):
      for y in range(0,self.height):
        self.tiles[(x,y)]=tile(x,y)
        if (x==0 or y==0 or x==self.width-1 or y==self.height-1): 
          self.tiles[(x,y)].passable=False
          self.tiles[(x,y)].underground="#"
    self.buildwall((4,6),(4,12))
    self.buildwall((14,6),(14,12))
    self.buildwall((6,4),(12,4))
    self.buildwall((6,14),(12,14))
    self.monsters=[]

  def populate(self):
    self.monsters.append(monster("goblin",(1,9)))
    self.monsters.append(monster("goblin",(2,10)))
    self.monsters.append(monster("goblin",(1,11)))
    self.monsters.append(monster("goblin",(1,12)))
    self.monsters.append(monster("orc",(5,15)))
    self.monsters.append(monster("orc",(4,13)))
    self.monsters.append(monster("ogre",(18,11)))

  def buildwall(self,start,end):
    if(start[0]==end[0]):
      for k in range(start[1],end[1]+1):
        self.tiles[(start[0],k)].passable=False
        self.tiles[(start[0],k)].underground="#"
    elif(start[1]==end[1]):
      for k in range(start[0],end[0]+1):
        self.tiles[(k,start[1])].passable=False
        self.tiles[(k,start[1])].underground="#"
    else: print("your wall is lean")

  def buildstaircase(self,x,y):
    if(self.tiles[(x,y)].passable):
      self.tiles[(x,y)].ground.append(staircase(self,None))

  def ascii_render(self):
    for y in range(0,self.width):
      for x in range(0,self.height):
        print(self.tiles[(x,y)].underground, sep="", end="")
      print("\n", sep="", end="")

###############################################################################
# a field
class tile(object):
  def __init__(self,x,y):
    self.posx=x
    self.posy=y
    self.passable=True
    self.underground="."
    self.actor=None
    self.ground=[]

###############################################################################
# TODO: stairs
class staircase(object):
  def __init__(self,dest):
    pass

  def use(self):
    pass

###############################################################################
# actor-class; everything that can move around in the dungeon (e.g. the player)
class actor(object):
  def __init__(self):
    self.posx=0
    self.posy=0
    self.name="unknown"
    self.sign="?"
    self.health=1
    self.mana=1
    self.tohit=0.5
    self.multi=1
    self.fatigued=False
    self.alive=True
    self.level=1
    self.xp=0

  def setpos(self,x,y):
    self.posx=x
    self.posy=y
    d.tiles[(self.posx,self.posy)].passable=False
    d.tiles[(self.posx,self.posy)].underground=self.sign
    d.tiles[(self.posx,self.posy)].actor=self

  def getpostile(self):
    return d.tiles[(self.posx,self.posy)]

  def move(self,x,y):
    if not (self.posx+y in range(0,d.height) and \
      self.posx+x in range(0,d.width)): return
    if not (d.tiles[(self.posx+x,self.posy+y)].passable):
      self.checkattack(x,y)
      return
    d.tiles[(self.posx,self.posy)].passable=True
    d.tiles[(self.posx,self.posy)].underground="."
    d.tiles[(self.posx,self.posy)].actor=None
    self.posx+=x
    self.posy+=y
    d.tiles[(self.posx,self.posy)].passable=False
    d.tiles[(self.posx,self.posy)].underground=self.sign
    d.tiles[(self.posx,self.posy)].actor=self
    self.fatigued=True

  def checkattack(self,x,y):
    target=d.tiles[(self.posx+x,self.posy+y)].actor
    if(target):
      self.attack(target)

  def attack(self, target):
    r=random.random()
    if(r<self.tohit): 
      print(self.name+" hit "+target.name, sep='')
      target.takedamage(random.randint(1,self.multi))
    else:
      print(self.name+" missed "+target.name)

  def takedamage(self, dam):
    self.health-=dam;
    print(self.name+" took "+str(dam)+" damage")
    if(self.health<=0): self.die()

  def ascii_render(self):
    print("actor at ", self.posx, self.posy)

###############################################################################

# the player
class hero(actor):
  def __init__(self):
    super(hero, self).__init__()
    self.name="player"
    self.sign="@"
    self.health=100
    self.mana=100
    self.tohit=0.7
    self.multi=10
    self.weapon=None
    self.armor=None
    self.inventory=None
  def grabitem(self):
    pass

  def equipitem(self):
    pass

  def die(self):
    d.tiles[(self.posx,self.posy)].actor=None
    d.tiles[(self.posx,self.posy)].underground="."
    d.tiles[(self.posx,self.posy)].passable=True
    self.alive=False
    print(self.name+" died")

  def ascii_render(self):
    print("hero "+self.name+" at ", self.posx, self.posy, "with "+ \
      str(self.health)+" health and "+str(self.mana)+" mana")
    #self.inventory.ascii_render()

###############################################################################
# simple item-class (without use yet)
class item(object):
  _name="default"
  _type="default"
  value=10

  def __init__(self, n, t):
    self.name=n
    self.type=t

  def equip(self):
    pass

  def ascii_render(self):
    print("item "+self.name+" of type "+self.type)

###############################################################################
# the inventory, also without use yet 
class inventory(object):
  def __init__(self):
    self.items=[]

  def additem(self, i):
    if not(isinstance(i, item)): print("notaitem")
    else: self.items.append(i)

  def showitem(self, i):
    pass

  def dropitem(self, i):
    pass

  def ascii_render(self):
    print("inventory contains:")
    for x in self.items: 
      x.ascii_render()

###############################################################################
# monsters - goblins, orcs and ogers 
# with stupid AI (move and attack) 
class monster(actor):
  def __init__(self, kind, pos):
    super(monster, self).__init__()
    self.target=None
    if kind is not None:
      if(kind=="goblin"):self.goblin()
      if(kind=="orc"):self.orc()
      if(kind=="ogre"):self.ogre()
      if(kind=="troll"):self.troll()
    if pos is not None:
      self.setpos(pos[0],pos[1])

  def goblin(self):
    self.name="goblin"
    self.sign="g"
    self.health=10
    self.mana=0
    self.tohit=0.33
    self.multi=3

  def orc(self):
    self.name="orc"
    self.sign="o"
    self.health=40
    self.mana=0
    self.tohit=0.5
    self.multi=5

  def ogre(self):
    self.name="Ogre"
    self.sign="O"
    self.health=120
    self.mana=0
    self.tohit=0.4
    self.multi=8

  def troll(self):
    self.name="Troll"
    self.sign="T"
    self.health=65
    self.mana=0
    self.tohit=0.5
    self.multi=6

  def act(self):
    if not(self.fatigued):
      if(self.alive):
        self.look()
        self.fatigued=True

  def look(self):
    maxxdist=8
    maxydist=8
    for j in range(self.posy-maxydist,self.posy+maxxdist):
      for i in range(self.posx-maxydist,self.posx+maxxdist):
        if not (j in range(0,d.height) and i in range(0,d.width)): continue
        if(isinstance(d.tiles[(i,j)].actor, hero)):
          self.target=d.tiles[(i,j)].actor
          self.moveTo(i,j)
          return

  def checkattack(self,x,y):
    target=d.tiles[(self.posx+x,self.posy+y)].actor
    if(isinstance(target, hero)):
      self.attack(target)
    else:
      pass

  def moveTo(self, tarx, tary):
    dx=abs(self.posx-tarx)
    dy=abs(self.posy-tary)

    if(self.posx-tarx<0): sx=1
    elif(self.posx-tarx==0): sx=0
    else: sx=-1;

    if(self.posy-tary<0): sy=1
    elif(self.posy-tary==0): sy=0
    else: sy=-1;

    if(dx>dy): self.move(sx,0) 
    elif(dx<dy): self.move(0,sy)
    elif(dx==dy): self.move(0,sy)
    else: pass

  def die(self):
    d.tiles[(self.posx,self.posy)].actor=None
    d.tiles[(self.posx,self.posy)].underground="."
    d.tiles[(self.posx,self.posy)].passable=True
    self.alive=False
    print(self.name+" died")

  def ascii_render(self):
    print("monster "+self.name+" at ", self.posx, self.posy, "with "+ \
      str(self.health)+" health and "+str(self.mana)+" mana")

###############################################################################
###############################################################################
# .
if __name__=="__main__":
  game=True
  d=dungeon()
  d.populate()
  p=hero()
  p.setpos(9,9)
  p.inventory=inventory()
  p.inventory.additem(item("longsword", "weapon"))
  p.inventory.additem(item("chainmail", "armor"))
  while(game):
    d.ascii_render() # "render" the dungeon in the console
    p.ascii_render() # show the player infos (hp, etc.) 
    for m in d.monsters:
      #m.ascii_render()
      m.fatigued=False
    key=input(":") # cheap controls :) 
    if(key=="w"): p.move(0,-1)
    if(key=="a"): p.move(-1,0)
    if(key=="s"): p.move(0,1)
    if(key=="d"): p.move(1,0)
    if(key=="x"): game=False
    for m in d.monsters:
      if(m.alive): m.act()
      else:
        del d.monsters[d.monsters.index(m)]
    if not(p.alive): game=False
