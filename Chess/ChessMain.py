"""
This is our main driver file . It will be responsible for handling user input and displaying the
current GameState Object
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 # dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animation later on
IMAGES = {}

'''
Initialize global dictionary of images. 
This will be called exactly once 
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp',  'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")
    #Note : we can access an image by saying 'IMAGE['wp']'

    '''
    The main driver for our code 
    '''

def main():
    p.init()
    screen       = p.display.set_mode((WIDTH, HEIGHT))
    clock        = p.time.Clock()
    screen.fill(p.Color("white"))
    gs           = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages()      # only once
    running      = True
    sqSelected   = () # no square is selected, keep track of the last click of the user
    playerClicks = [] # keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected   = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: # second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () # reset user clicks
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen , gs):
    drawBoard(screen) # draw squares on the board
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("gray"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[row][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()



