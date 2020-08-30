import pygame, sys, random, numpy
from pygame.locals import *

def getRandomizedBoard():
    """icons = [pygame.image.load("bit1.png").convert(), pygame.image.load("bit2.png").convert(),
             pygame.image.load("bit3.png").convert(),
             pygame.image.load("bit4.png").convert(), pygame.image.load("bit5.png").convert(),
             pygame.image.load("bit6.png").convert(),
             pygame.image.load("bit7.png").convert(), pygame.image.load("bit8.png").convert(),
             pygame.image.load("bit9.png").convert(),
             pygame.image.load("bit10.png").convert(), pygame.image.load("bit11.png").convert(),
             pygame.image.load("bit12.png").convert(),
             pygame.image.load("bit13.png").convert(), pygame.image.load("bit14.png").convert(),
             pygame.image.load("bit15.png").convert()]"""

    icons = [pygame.image.load("Amol.jpg").convert(), pygame.image.load("Zantye.jpg").convert(),
             pygame.image.load("Ritika.jpg").convert(),
             pygame.image.load("Farhan.jpg").convert(), pygame.image.load("Payal.jpg").convert(),
             pygame.image.load("Sanika.jpg").convert(),
             pygame.image.load("Chinmay.jpg").convert(), pygame.image.load("Kenil.jpg").convert(),
             pygame.image.load("Satz.jpg").convert(),
             pygame.image.load("Rishab.jpg").convert(), pygame.image.load("Vishal.jpg").convert(),
             pygame.image.load("Khushboo.jpg").convert(),
             pygame.image.load("Dhruv.jpg").convert(), pygame.image.load("Karan.jpg").convert(),
             pygame.image.load("Ish.png").convert()]

    copyArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12, 13, 14, 15]
    icons = icons[:] * 2  # make two of each

    list1_shuf = []
    list2_shuf = []
    index_shuf = list(range(len(icons)))
    random.shuffle(index_shuf)
    for i in index_shuf:
        list1_shuf.append(icons[i])
        list2_shuf.append(copyArray[i])

    icons=list1_shuf
    copyArray=list2_shuf


    # Create the board data structure, with randomly placed icons.
    board = []
    refArray=[]
    for x in range(5):
        column = []
        refColumn=[]
        for y in range(6):
            column.append(icons[0])
            refColumn.append(copyArray[0])
            del icons[0]  # remove the icons as we assign them
            del copyArray[0]
        board.append(column)
        refArray.append(refColumn)

    temp=numpy.array(refArray)
    #Printing solution set
    print(temp)

    return board,refArray


def drawBoard(mainBoard, revealedBoxes):
    for x in range(0, 5):
        for y in range(0, 6):
            if (revealedBoxes[x][y] == 0):
                gameSurface.blit(mainBoard[x][y], (100 * (y + 1), 100 * (x + 1)))
            else:
                pygame.draw.rect(gameSurface, (255, 255, 255), (100 * (y + 1), 100 * (x + 1), 90, 90))


def getBoxAtPixel(mousex, mousey):  # we pass mousex and mousey here
    if 100 <= mousex <= 700 and 100 <= mousey <= 600:
        return ((mousex // 100) * 100, (mousey // 100) * 100)
    else:
        return (None, None)

def gameWonAnimation(board,revealedBoxes):
    # Flash the background color when the player has won
    color1 = (100, 100, 100)
    color2 = (60, 60, 100)

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        gameSurface.fill(color1)
        drawBoard(board, revealedBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def main():
    global gameSurface
    pygame.init()
    gameSurface = pygame.display.set_mode((800, 700))
    clock = pygame.time.Clock()
    #print(pygame.font.get_fonts())
    font = pygame.font.SysFont('arial',30)
    firstClick=False
    gameOver=False
    frame_count = 0
    frame_rate = 60
    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    zeroArray = numpy.zeros((5, 6), dtype=int)

    firstSelection = None  # stores the (x, y) of the first box clicked.
    gameSurface.fill((56, 142, 142))
    revealedBoxes = [[1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1]]
    mainBoard , referenceArray= getRandomizedBoard()
    drawBoard(mainBoard, zeroArray)
    pygame.display.update()
    pygame.time.wait(2000)

    while True:  # main game loop
        mouseClicked = False
        gameSurface.fill((56, 142, 142))  # drawing the window

        if firstClick == True:
            # Redraw the screen and wait a clock tick.
            total_seconds = frame_count // frame_rate

            # Divide by 60 to get total minutes
            minutes = total_seconds // 60

            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60

            # Use python string formatting to format in leading zeros
            output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

            text = font.render(output_string, True, (0, 0, 0))
            gameSurface.blit(text, [50, 50])
            gameSurface.blit(font.render("Memory Puzzle", True, (0, 0, 0)), [400, 50])

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                firstClick=True

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None:
            boxx = (boxx // 100) - 1
            boxy = (boxy // 100) - 1

            if mouseClicked == True:
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                    revealedBoxes[firstSelection[1]][firstSelection[0]] = 0

                else:  # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    revealedBoxes[boxy][boxx] = 0
                    drawBoard(mainBoard, revealedBoxes)
                    pygame.display.update()

                    if referenceArray[firstSelection[1]][firstSelection[0]] != referenceArray[boxy][boxx]:
                        # Icons don't match. Re-cover up both selections.
                        revealedBoxes[boxy][boxx] = 1
                        revealedBoxes[firstSelection[1]][firstSelection[0]] = 1
                        pygame.time.wait(1000)
                    else:
                        flag=0
                        for x in range(5):
                            for y in range(6):
                                if(revealedBoxes[x][y]==1):
                                    flag=1
                                    break
                        if(flag==0):
                            gameOver=True

                            gameWonAnimation(mainBoard,revealedBoxes)
                            pygame.time.wait(2000)

                            # Reset the board
                            main()
                            """mainBoard, referenceArray = getRandomizedBoard()
                            revealedBoxes = [[1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1],
                                             [1, 1, 1, 1, 1, 1]]

                            # Show the fully unrevealed board for a second.
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            gameOver = False
                            # Replay the start game animation.
                           # startGameAnimation(mainBoard)
                            
                            #gameSurface.fill((56, 142, 142))
                           # text = font.render("Game Over", True, (0, 0, 0))
                            #gameSurface.blit(text, [400, 350])
                            #pygame.display.update()"""


                    firstSelection = None

        if gameOver == False:
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            frame_count += 1

            # Limit frames per second
            clock.tick(frame_rate)
            drawBoard(mainBoard, revealedBoxes)
            pygame.display.update()

if __name__ == '__main__':
    main()
