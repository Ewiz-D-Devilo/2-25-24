import socket
from tkinter import *
from threading import Thread
import random
from PIL import ImageTk,Image

screen_width=None
screen_height=None

server=None
port=None
ip_address=None

playerName=None

canvas1=None
canvas2=None
NameEntry=None
nameWindow=None
gameWindow=None

leftBoxes=[]
rightBoxes=[]
finishBoxes=None

playerType=None
playerTurn=None

player1Name='joining....'
player2Name='joining......'
player1Label=None
player2Label=None
player1Score=0
player2Score=0

player1Scorelabel=None
player2Scorelabel=None

dice=None
rollButton=None
resetButton=None
winningMessage=None
winningFunctionCall=None

def rollDice():
    global server
    diceFaceVale=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    value= random.choice(diceFaceVale)

    print("DiceValue is:",value)

    global playerType,rollButton,playerTurn

    rollButton.destroy()
    playerTurn=False

    if(playerType == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())

    if(playerType == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode()) 

def checkPosition(boxes,color):
    for box in boxes:
        boxColor= box.cget("bg")
        if(boxColor == color):
            return boxes.index(box)
        
    return False

def movePlayer1(steps):
    global leftBoxes

    boxPosition= checkPosition(leftBoxes[1:],"red")

    if(boxPosition):
        diceValue= steps
        coloredBoxedIndex= boxPosition
        totalSteps=10
        remainingSteps= totalSteps-coloredBoxedIndex

        print("dicevalue",diceValue)
        print("cbi:",coloredBoxedIndex)
        print("remainingSteps:",remainingSteps)

        if(steps == remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg="white")

                finishBoxes.configure(bg="red")
                grtMsg= f"Red wins the game"
                SERVER.send(grtMsg.encod())
        elif steps < remainingSteps:
            for box in leftBoxes[1:]:
                box.configure(bg="white")

            nextStep=(coloredBoxedIndex+1)+ diceValue
            leftBoxes[nextStep].configure(bg="red")

        else:
            print("moveplayerisfalse")
    else:
        leftBoxes[steps].configure(bg="red")

def movePlayer2(steps):
    global rightBoxes,finishBoxes,SERVER,playerName
    boxPosition= checkPosition(leftBoxes[-2:-1],"yellow")

    if(boxPosition):
        diceValue= steps
        coloredBoxedIndex= boxPosition
        totalSteps=10
        remainingSteps= totalSteps-coloredBoxedIndex

        print("dicevalue",diceValue)
        print("cbi:",coloredBoxedIndex)
        print("remainingSteps:",remainingSteps)

        if(steps == remainingSteps):
            for box in rightBoxes[1:]:
                box.configure(bg="white")

                finishBoxes.configure(bg="green",fg="black")
                grtMsg= f"Red wins the game"
                SERVER.send(grtMsg.encod())

        elif steps < remainingSteps:
            for box in rightBoxes[1:]:
                box.configure(bg="white")

            nextStep=(coloredBoxedIndex+1)+ diceValue
            rightBoxes[::-1][nextStep].configure(bg="green")
        else:
            print("moveplayerisfalse")
    else:
        rightBoxes[len(rightBoxes)-(steps+1)].configure(bg="red")
    

def handleWinMsg(message):
    global SERVER, playerType,playerTurn,rollButton,screen_height,screen_width,canvas2,gameWindow,playerName,player1Name,player2Name,player1Label,player2Label,winningFunctionCall

    if('red' in message):
        if(playerType =="Player2"):
            rollButton.destroy()

    if ('green' in message):
        if(playerType== "player1"):
            rollButton.destroy()

    message= message.split(".")[0]
    canvas2.itemconfigure(winningMessage,text=message)

    resetButton.place(x=screen_width/2-100,y=screen_height/2+250)

def updateScore(message):
    global SERVER, playerType,playerTurn,rollButton,screen_height,screen_width,canvas2,gameWindow,playerName,player1Name,player2Name,player1Label,player2Label,winningFunctionCall,player1Score,player2Score
    
    if('red' in message):
        player1Score+=1
    if('yellow'in message):
        player2Score+=1

    canvas2.itemconfigure(player1Scorelabel,text=player1Score)
    canvas2.itemconfigure(player2Scorelabel,text=player2Score)

def resetGame():
    global SERVER, playerType,playerTurn,rollButton,screen_height,screen_width,canvas2,gameWindow,playerName,player1Name,player2Name,player1Label,player2Label,winningFunctionCall,player1Score,player2Score

    canvas2.itemconfigure(dice,text='\u2680')
    if(playerType == 'player1'):
        rollButton=Button(gameWindow,text="roll a dice",font=("Chalkboard SE",20),width=12,height=1,bg="white",bd=1,command=rollDice)
        rollButton.place(x=screen_width/2-100 , y=screen_height/2 +150)
        playerTurn=True

    if(playerType == 'player2'):
        playerTurn=False

    for r in rightBoxes[-2:-1]:
        r.configure(bg="white")

    for l in leftBoxes[1:]:
        l.configure(bg="white")

    finishBoxes.configure(bg="green")
    canvas2.itemconfigure(winningMessage,text="")
    resetButton.destroy()

    resetButton=Button(gameWindow,text="reset luh game",font=("Chalkboard SE",20),width=12,height=1,bg="white",bd=1)
    winningFunctionCall=0


def receiveMsg():
    global SERVER, playerType,playerTurn,rollButton,screen_height,screen_width,canvas2,gameWindow,playerName,player1Name,player2Name,player1Label,player2Label,winningFunctionCall

    while True:
        message= SERVER.recv(2048).decode()
        print("what msg receiveing" , message)
        if('player_type' in message):
            recvMsg=eval(message)
            playerType= recvMsg['player_type']
            playerTurn= recvMsg['turn']

        elif('player_name' in message):
            players=eval(message)
            players=players['player_name']

            for p in players:
                if[p["type"]=="player1"]:
                    player1Name=p["name"]
                if[p["type"]=="player2"]:
                    player2Name=p["name"]
        elif ('⚀' in message):
            canvas2.itemconfigure(dice,text='\u2680')
        elif ('⚁' in message):
            canvas2.itemconfigure(dice,text='\u2681')
        elif ('⚂' in message):
            canvas2.itemconfigure(dice,text='\u2682')
        elif ('⚃' in message):
            canvas2.itemconfigure(dice,text='\u2683')
        elif ('⚄' in message):
            canvas2.itemconfigure(dice,text='\u2684')
        elif ('⚅' in message):
            canvas2.itemconfigure(dice,text='\u2685')

        elif ('wins the game' in message):
            handleWinMsg(message)
            winningFunctionCall+=1
            updateScore(message)

        elif (message =="reset game"):
            resetGame()

        #rollbutton
        if('player1Turn' in message and playerType =="player1"):
            rollButton=Button(gameWindow,text="roll a dice",font=("Chalkboard SE",20),width=12,height=1,bg="white",bd=1,command=rollDice)
            rollButton.place(x=screen_width/2-100 , y=screen_height/2 +150)
            playerTurn=True

        elif('player2Turn' in message and playerType =="player2"):
            rollButton=Button(gameWindow,text="roll a dice",font=("Chalkboard SE",20),width=12,height=1,bg="white",bd=1,command=rollDice)
            rollButton.place(x=screen_width/2-100 , y=screen_height/2 +150)
            playerTurn=True

        #deciding which player takes turn
        if('player1Turn' in message or 'player2Turn'in message):
            diceChoices=['⚀','⚁','⚂','⚃','⚄','⚅']
            dicevalue= diceChoices.index(message[0])+1
            if('player2Turn' in message):
                movePlayer1(dicevalue)
            if('player1Turn' in message):
                movePlayer2(dicevalue)

        if(player1Name != 'joining' and canvas2):
            canvas2.itemconfigure(player1Label,text=player1Name)

        if(player2Name != 'joining' and canvas2):
            canvas2.itemconfigure(player2Label,text=player2Name)



def welcomeScreen():
    global NameEntry,nameWindow,canvas1,playerName

    nameWindow=Tk()
    nameWindow.title("welcome!")
    nameWindow.attributes('-fullscreen',True)

    screen_width=nameWindow.winfo_screenwidth()
    screen_height=nameWindow.winfo_screenheight()

    canvas1=Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill="both",expand=True)

    bg=ImageTk.PhotoImage(file='background.png')
    canvas1.create_image(0,0,image=bg,anchor="nw")
    canvas1.create_text(screen_width/2,screen_height/5,text="ENTER YOUR NAME",font=("Chalkboard SE",80),fill="white")
    
    NameEntry=Entry(nameWindow,width=15,justify="center",font=("Chalkboard SE",50),bd=5,bg='white')
    NameEntry.place(x=screen_width/2-230,y=screen_height/2-200)

    button=Button(nameWindow,text="Save",font=("Chalkboard SE",20),width=12,height=1,bg="green",bd=1,command=navigate_gameRoom)
    button.place(x=screen_width/2-200,y=screen_height/2-50)
    
    print(screen_width,screen_height)
    nameWindow.mainloop()


def create_leftboxes():
    global gameWindow,leftBoxes,screen_height,screen_width

    xpos=10
    for box in range(0,11):
        if(box == 0):
            boxLabel=Label(gameWindow,font=("Chalkboard SE",30),width=1,height=1,relief='ridge',bg="red",borderwidth=0)
            boxLabel.place(x=xpos,y=screen_height/2 - 100)
            leftBoxes.append(boxLabel)
            xpos+=30
        else:
            boxLabel=Label(gameWindow,font=("Chalkboard SE",30),width=1,height=1,relief='ridge',bg="white",borderwidth=0)
            boxLabel.place(x=xpos,y=screen_height/2 - 100)
            leftBoxes.append(boxLabel)
            xpos+=55

def create_rightboxes():
    global gameWindow,rightBoxes,screen_height,screen_width

    xpos=1300
    for box in range(0,11):
        if(box == 10):
            boxLabel=Label(gameWindow,font=("Chalkboard SE",30),width=1,height=1,relief='ridge',bg="green",borderwidth=0)
            boxLabel.place(x=xpos,y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xpos+=30
        else:
            boxLabel=Label(gameWindow,font=("Chalkboard SE",30),width=1,height=1,relief='ridge',bg="white",borderwidth=0)
            boxLabel.place(x=xpos,y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xpos+=55

def homebox():
    global gameWindow,finishBoxes,screen_height,screen_width

    finishBoxes=Label(gameWindow,text="home",font=("Chalkboard SE",30),width=5,height=0,borderwidth=2,bg="green",fg="white")
    finishBoxes.place(x=screen_width/2-50 , y=screen_height/2-80)

def gameScreen():
    global playerName,screen_height,screen_width,canvas2,player1Label,player2Label,player1Score,player2Score,player1Scorelabel,player2Scorelabel
    global gameWindow,player1Name,player2Name,rollButton,resetButton,winningMessage,resetButton,dice

    gameWindow=Tk()
    gameWindow.title("Game")
    gameWindow.attributes('-fullscreen',True)

    screen_width=gameWindow.winfo_screenwidth()
    screen_height=gameWindow.winfo_screenheight()

    canvas2=Canvas(gameWindow,width=500,height=500)
    canvas2.pack(fill="both",expand=True)
    
    bg=ImageTk.PhotoImage(file='background.png')
    canvas2.create_image(0,0,image=bg,anchor="nw")
    canvas2.create_text(screen_width/2,screen_height/5+100,text="ENTER YOUR NAME",font=("Chalkboard SE",70),fill="white")

    rollButton=Button(gameWindow,text="roll a dice",font=("Chalkboard SE",20),width=12,height=1,bg="white",bd=1,command=rollDice)
    if(playerType == "player1" and playerTurn):
        rollButton.place(x=screen_width/2-100,y=screen_height/2+150)
    else:
        rollButton.pack_forget()
    
    dice=canvas2.create_text(screen_width/2,screen_height/2+50,text='\u2681',font=("Chalkboard SE",100),fill="white")

    player1Label=canvas2.create_text(screen_width/6,screen_height/2-400,text=player1Name,font=("Chalkboard SE",100),fill="white")
    player2Label=canvas2.create_text(screen_width/6+1300,screen_height/2-400,text=player2Name,font=("Chalkboard SE",100),fill="white")

    player1Scorelabel=canvas2.create_text(screen_width/6,screen_height/2-300,text=player1Score,font=("Chalkboard SE",100),fill="white")
    player2Scorelabel=canvas2.create_text(screen_width/6+1300,screen_height/2-300,text=player2Score,font=("Chalkboard SE",100),fill="white")

    resetButton=Button(gameWindow,text="reset luh game",font=("Chalkboard SE",20),width=12,height=1,bg="white",bd=1)
    resetButton.place(x=screen_width/2-100,y=screen_height/2+250)


    create_leftboxes()
    create_rightboxes()
    homebox()
    gameWindow.mainloop()
#gameScreen()

def navigate_gameRoom():
    global SERVER,nameWindow,NameEntry,playerName
    playerName=NameEntry.get()
    NameEntry.delete(0,END)
    nameWindow.destroy()
    SERVER.send(playerName.encode())
    gameScreen()

def setup():
    global SERVER,PORT,ip_address
    ip_address='127.0.0.1'
    port=8000
    SERVER= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((ip_address,port))
    recv= Thread(target=receiveMsg)
    recv.start()
    welcomeScreen()
    
   

setup()