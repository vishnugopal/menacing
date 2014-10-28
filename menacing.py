import pickle, random
from sys import argv, exit

def resetDumb():
    "Used to reset the save file to a dumb version"
    matchboxes = {}
    matchboxes['BBBBBBBBB'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']    
    pickle.dump(matchboxes, open('save.txt','w'))
    print "Matchboxes reset to a dumb version."

def skewMatchboxes(result):
    global matchboxes, newbox, debugstate
    if result == 'O':
        for state, bead in newbox.items():
            if debugstate:
                print "Removing", bead, "from", state,
            if matchboxes[state].count(bead) > 0:
                matchboxes[state].remove(bead)
            if debugstate:
                print matchboxes[state]
    elif result == 'X': 
        for state, bead in newbox.items():
            if debugstate:
                print "Adding", bead, "to", state,
            matchboxes[state].append(bead)
            if debugstate:
                print matchboxes[state]

def loadMatchboxes(file = 'save.txt'):
    "Loads matchboxes from a saved file"
    global matchboxes, debugstate
    if debugstate:
        print "Loading matchboxes from saved file."
    try:
        matchboxes = pickle.load(open(file, 'r'))
    except IOError:
        print "No save file found, try running --init"

def dumpMatchboxes(file = 'save.txt'):
    "Dump state to file"
    global matchboxes, debugstate
    if debugstate:
        print "Saving matchboxes to file."
    pickle.dump(matchboxes, open('save.txt', 'w'))

def trainerMove():
    "Move trainer"
    global boardstate
    bead = winningMove('X')
    bead2 = winningMove('O')
    if bead:
        move = translateToPosition(bead)
    elif bead2:
        move = translateToPosition(bead2)
    else:
        move = ""
        while not validMove(move):
            move = random.randint(0, 8)
    boardstate[move] = 'O'

def trainComputer(iter = 200):
    "Trains the computer automatically by playing it against another computer"
    global boardstate, matchboxes, newbox, debugstate

    computer = 0
    trainer = 0
    draw = 0
    
    print "Loading matchboxes from saved file"
    loadMatchboxes()
    for i in range(0, iter + 1):
        boardstate = ['B'] * 9
        newbox = {}
        print "Playing iteration: ", i,

        #Pick player/trainer to start at random    
        move = random.randint(0, 1)
        if move:
            computerMove()
            move = computerMove
        else:
            trainerMove()
            move = trainerMove

        #Iterate until a winning/draw situation        
        while not winningBoard():
            if move == computerMove:
                trainerMove()
                move = trainerMove
            else:
                move = computerMove
                computerMove()
        result = winningBoard()
        if result == 'O':
            print "Trainer won"
            trainer += 1
        elif result == "Draw":
            print "Draw"
            draw += 1
        else:
            print "Computer won"
            computer += 1
        skewMatchboxes(result)
    print "Results: Computer: ", computer, "Trainer", trainer, "Draws", draw
    print "Saving matchboxes"
    dumpMatchboxes()   

def showState():
    "Shows the current data in the saved file"
    matchboxes = pickle.load(open('save.txt', 'r'))
    print matchboxes

def translateToPosition(string):
    "Translate a bead color to a position"
    translator = {'A': 0, 'B': 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6,
                  'H' : 7, 'I' : 8}
    return translator[string]

def translateToBead(num):
    "Translate a position to a bead color"
    translator = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                  'H', 'I']
    return translator[num]

def validMove(pos):
    "Tests whether the given move is valid"
    if pos > 8:
        return 0
    if pos == "":
        return 0
    global boardstate
    if boardstate[pos] == 'B':
        return 1
    else:
        return 0

def boardstateToString():
    "Converts boardstate array to a conjugated string"
    global boardstate
    y = ""
    for x in boardstate:
        y += x
    return y
    
def winningMove(player = 'X'):
    "Gets a winning move if it exists"
    global boardstate
    #Horizontal
    for i in [0, 3, 6]:
        if(boardstate[i] == boardstate[i + 1] == player and boardstate[i + 2] == 'B'):
            return translateToBead(i + 2)
        if(boardstate[i] == boardstate[i + 2] == player and boardstate[i + 1] == 'B'):
            return translateToBead(i + 1)
        if(boardstate[i + 1] == boardstate[i + 2] == player and boardstate[i] == 'B'):
            return translateToBead(i)
    #Vertical
    for i in [0, 1, 2]:
        if(boardstate[i] == boardstate[i + 3] == player and boardstate[i + 6] == 'B'):
            return translateToBead(i + 6)
        if(boardstate[i] == boardstate[i + 6] == player and boardstate[i + 3] == 'B'):
            return translateToBead(i + 3)
        if(boardstate[i + 3] == boardstate[i + 6] != 'B' and boardstate[i] == 'B'):
            return translateToBead(i)
    #Diagonal
    if(boardstate[0] == boardstate[4] == player and boardstate[8] == 'B'):
        return translateToBead(8)
    if(boardstate[0] == boardstate[8] == player and boardstate[4] == 'B'):
        return translateToBead(4)
    if(boardstate[4] == boardstate[8] == player and boardstate[0] == 'B'):
        return translateToBead(0)
    if(boardstate[2] == boardstate[4] == player and boardstate[6] == 'B'):
        return translateToBead(6)
    if(boardstate[2] == boardstate[6] == player and boardstate[4] == 'B'):
        return translateToBead(4)
    if(boardstate[4] == boardstate[6] == player and boardstate[2] == 'B'):
        return translateToBead(2)
    #No winning move    
    return 0

def winningBoard():
    "Outputs the winning player, not won yet, or draw"
    global boardstate
    
    #Horizontal
    if(boardstate[0] == boardstate[1] == boardstate[2] != 'B'):
        return boardstate[0]
    if(boardstate[3] == boardstate[4] == boardstate[5] != 'B'):
        return boardstate[3]
    if(boardstate[6] == boardstate[7] == boardstate[8] != 'B'):
        return boardstate[6]
    #Vertical
    if(boardstate[0] == boardstate[3] == boardstate[6] != 'B'):
        return boardstate[0]
    if(boardstate[1] == boardstate[4] == boardstate[7] != 'B'):
        return boardstate[1]
    if(boardstate[2] == boardstate[5] == boardstate[8] != 'B'):
        return boardstate[2]
    #Diagonal
    if(boardstate[0] == boardstate[4] == boardstate[8] != 'B'):
        return boardstate[0]
    if(boardstate[2] == boardstate[4] == boardstate[6] != 'B'):
        return boardstate[2]

    #Draw
    flag = 1
    for x in boardstate:
        if x == 'B':
            flag = 0
    if flag == 1:
        return "Draw"


    #Not winning
    return 0


def printBoard():
    "Prints a formatted board"
    global boardstate
    count = 0
    for x in boardstate:
        if (count % 3 == 0):
            print
        if x == 'B':
            print ' ',
        else:
            print x,        
        print ' | ' ,
        count += 1
    print


def computerMove():
    "This is how a computer moves, stores new moves in newbox. Computer moves with X."
    global boardstate, matchboxes, newbox, debugstate
                
    boardstate_string = boardstateToString() #Hash boardstate
    
    try:
        beads = matchboxes[boardstate_string]
        if beads == []:
            if debugstate:
                print "The beads became empty, reinitializing"
            matchboxes[boardstate_string] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    except KeyError:
        if debugstate:
            print "New state found, matchbox initializing"
        matchboxes[boardstate_string] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    if debugstate:
        print "Pruning invalid moves"
    
    for y in range(0, len(boardstate)):
        x = boardstate[y]
        if x != 'B':
            if matchboxes[boardstate_string].count(translateToBead(y)) > 0:
                matchboxes[boardstate_string].remove(translateToBead(y))
            
    if debugstate:
        print "Beads in matchbox: ", boardstate_string, matchboxes[boardstate_string]                
    
    beads = matchboxes[boardstate_string]

    bead = 0
    bead = winningMove('X')
    if bead: #If there is a winning move for X
        if debugstate:
            print "Processing winning move for X."
        move = translateToPosition(bead)    
    else:
        bead = 0
        bead = winningMove('O')
        if bead: #If there is a winning move for O
            if debugstate:
                print "Processing winning move for O."
            move = translateToPosition(bead)
        else:
            move = ""
            while not validMove(move):
                bead = random.choice(beads)
                move = translateToPosition(bead)
                if debugstate:
                    print "Selected bead", bead, "Processing move: ", move + 1
    newbox[boardstate_string] = bead
    boardstate[move] = 'X'

def playerMove():
    "Player move, just checks for valid moves. Player moves with O."
    global boardstate
    print "To play, enter the board position you want to put a circle in (1-9)."
    move = ""
    while not validMove(move):
        try:
            move = int(raw_input('> ')) - 1
        except ValueError:
            pass
        except KeyboardInterrupt:
            print 
            print "Thanks for playing"
            exit(0)
        if not validMove(move):
            print "Not valid move."
    boardstate[move] = 'O'
    pass

def main():
    """
    Menacing v0.9
    Welcome to Menacing. Menacing is an emulation of MENACE
    developed in 1960 by an English biologist named Donald
    Michie. It stays fairly true to the original MENACE
    simulation, and has both positive and negative
    reinforcements. To learn more about MENACE, go to
    http://www.atarimagazines.com/v3n1/matchboxttt.html

    Usage
    
        menacing [params]
        --state
          gets the current state of the matchboxes
        --reset
        --init
          resets the saved matchboxes to a dumb version.
        --train [iterations]
          trains the matchboxes using computer vs. computer.
          iterations defaults to 200.
        --debug enables debug mode
                  
    """

    global boardstate, matchboxes, newbox, debugstate

    #Initialize a blank board
    boardstate = ['B'] * 9

    #Set debugstate to off
    debugstate = 0

    #Initialize a dictionary for new moves    
    newbox = {}
        
    #process arguments
    if len(argv) > 1:
        param = argv[1]
        if param == "--state":
            showState()
            exit(0)
        if param == '--reset' or param == '--init':
            resetDumb()
            exit(0)
        if param == '--train':
            try:
                if argv[2]:
                    trainComputer(int(argv[2]))
                    exit(0)
            except IndexError:
                pass
            trainComputer()
            exit(0)
        if param == '--debug':
            debugstate = 1

    print "Press Ctrl+C to quit"
        
    loadMatchboxes()    

    #Pick player/computer to start at random    
    move = random.randint(0, 1)
    if move:
        computerMove()
        move = computerMove
        printBoard()
    else:
        printBoard()
        playerMove()
        move = playerMove

    #Iterate until a winning/draw situation        
    while not winningBoard():
        if move == computerMove:
            playerMove()
            move = playerMove
            if winningBoard():
                printBoard()
        else:
            move = computerMove
            computerMove()
            printBoard()

    result = winningBoard()

    if result == 'Draw':
        print "Draw"
    else:
        print "Winner", result

    skewMatchboxes(result)

    dumpMatchboxes()
        
if __name__ == "__main__":
    print main.func_doc
    main()

