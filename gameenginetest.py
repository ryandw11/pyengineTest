import pyengine as gm
from pyengine import GameObjectManager
from pyengine import Rectange
from pyengine import KeyHandler
import pygame
import random

# Example game using the PyEngine HAPI for pygame


engine = gm.PYEngineBuilder([1000, 700]).setTitle("ExampleGame").setSpeed(100).build()

img = gm.Sprite().setImage("thetot.jpg").setPosition((200, 200))
GameObjectManager.add(img)

player = Rectange().setPosition([1000/2, 500]).setColor([0, 0, 255])
GameObjectManager.add(player)

ground = Rectange().setPosition([0, 650]).setSize((1500, 50)).setColor((0, 255, 0))
GameObjectManager.add(ground)

text = gm.Text().setPosition([800, 30]).setColor([0, 0, 0]).setText("Score: 0").setTextSize(70)
GameObjectManager.add(text)

inJump = False
currentPosition = [0, 0]

def jump():
    global inJump
    if player.position[1] > currentPosition[1] - 300:
        player.translate([0, -10])
    else:
        inJump = False

time = 2.0
countDown = 2.0
gameOver = False

def spawnObject(e):

    if gameOver: return

    global countDown
    global time
    countDown -= gm.deltaTime

    if countDown / 1000 < 0:
        if time > 0.5:
            time -= random.random() / 50
        countDown = time
        makeObject()


activeObjs = []
def makeObject():
    obj = Rectange().setPosition([1450, 600]).setColor((255, 0, 0)).setSize([50, 50])
    GameObjectManager.add(obj)
    activeObjs.append(obj)


speed = -1.5
playerScore = 0


def moveObject(e):
    global speed
    global gameOver
    global playerScore
    if gameOver: return
    for i in range(len(activeObjs)):
        activeObjs[i].translate([-25, 0])
        if activeObjs[i].position[0] < 0:
            GameObjectManager.remove(activeObjs[i])
            activeObjs.remove(activeObjs[i])
            speed -= random.random() / 100
            playerScore += 1

def handleText(e):
    global playerScore
    if gameOver:
        text.setText("Game Over").setColor((255, 0, 0))
    else:
        text.setText("Score: " + str(playerScore))

def collide(e):
    global gameOver
    for i in activeObjs:
        if gm.CollisionManager.isColliding(player, i):
            gameOver = True
            engine.stop()


def onKey(e):
    if gameOver: return
    global inJump
    global currentPosition
    global player

    if (KeyHandler.isKeyPressed(pygame.K_UP)) & (not inJump) & (gm.CollisionManager.isColliding(player, ground)):
        currentPosition = player.position
        inJump = True

    if inJump:
        jump()
    elif not gm.CollisionManager.isColliding(player, ground):
        player.translate([0, 10])


gm.EventHandler.addHandler("UpdateEvent", onKey)
gm.EventHandler.addHandler("UpdateEvent", spawnObject)
gm.EventHandler.addHandler("UpdateEvent", moveObject)
gm.EventHandler.addHandler("UpdateEvent", handleText)
gm.EventHandler.addHandler("UpdateEvent", collide)

engine.start()