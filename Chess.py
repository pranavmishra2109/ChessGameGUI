from copy import*
from graphics import*
#V21.4 - editing comments in function makeMove

def showLegalMoves(gWin):
  for rowIndex in range(0, 8):
    for blockIndex in range(0, 8):
      if 'l' in chessBoardList[rowIndex][blockIndex]:
        legalXLL = (blockIndex + 1) * 40
        legalXUR = legalXLL + 40
        legalYLL = (rowIndex + 1) * 40
        legalYUR = legalYLL + 40
        if 'e' in chessBoardList[rowIndex][blockIndex]:
          greyCircle = Circle(Point((legalXLL + legalXUR)/2,(legalYLL + legalYUR)/2), 10)
          greyCircle.setFill(color_rgb(128, 128, 128))
          greyCircle.setOutline(color_rgb(128, 128, 128))
          greyCircle.draw(gWin)
        else:
          textOfPiecePresentWithLegalMark = chessBoardList[rowIndex][blockIndex]
          textOfPiecePresent = textOfPiecePresentWithLegalMark[0:int(len(textOfPiecePresentWithLegalMark)-1)]
          unicodeOfPiecePresent = pieceUnicodes[textOfPiecePresent]
          pieceInDanger = Text(Point((legalXLL + legalXUR)/2,(legalYLL + legalYUR)/2), unicodeOfPiecePresent)
          pieceInDanger.setTextColor('red')
          pieceInDanger.setSize(30)
          pieceInDanger.draw(gWin)

def isCheckMate(thePiece):
  numOfLegalMovesToPreventCheck = 0
  legalMovesToPreventCheck = {}
  oppColorPiecesDictionary = {}
  tempList = deepcopy(chessBoardList)
  #print("The list before checking for checkmate should not have any legal marker: ")
  #print(tempList)
  for rowIndex in range(8):
    for blockIndex in range(8):
      oppColorIndexes = ""
      if (tempList[rowIndex][blockIndex])[0] != 'e' and (tempList[rowIndex][blockIndex])[0] != thePiece[0]:
        oppColorIndexes = str(rowIndex) + " " + str(blockIndex)
        oppColorPiecesDictionary.update({oppColorIndexes:tempList[rowIndex][blockIndex]})

  #print(oppColorPiecesDictionary)

  for oppColorIndexes in oppColorPiecesDictionary.keys():
    legalMovesOfAPiece = []
    indexesNeeded = oppColorIndexes.split()
    rowIndexNeeded = int(indexesNeeded[0])
    blockIndexNeeded = int(indexesNeeded[1])
    #print("Getting Legal Moves for: "+oppColorPiecesDictionary[oppColorIndexes])
    getPossibleMoves(rowIndexNeeded, blockIndexNeeded, oppColorPiecesDictionary[oppColorIndexes], tempList)
    filterLegalMoves(rowIndexNeeded, blockIndexNeeded, oppColorPiecesDictionary[oppColorIndexes], tempList)
    #print("These are the legal moves for piece "+oppColorPiecesDictionary[oppColorIndexes])
    #print(tempList)
    for rowIndex in range(8):
      for blockIndex in range(8):
        particularLegalMove = []
        if 'l' in tempList[rowIndex][blockIndex]:
          #print("legal move found")
          particularLegalMove.append(rowIndex)
          particularLegalMove.append(blockIndex)
          legalMovesOfAPiece.append(particularLegalMove)

    for rowIndex in range(8):
      for blockIndex in range(8):
        if 'l' in tempList[rowIndex][blockIndex]:
          block = tempList[rowIndex][blockIndex]
          tempList[rowIndex][blockIndex] = block[0:int(len(block)-1)]

    legalMovesToPreventCheck.update({oppColorPiecesDictionary[oppColorIndexes]:legalMovesOfAPiece})

  for saviourMoves in legalMovesToPreventCheck.values():
    numOfLegalMovesToPreventCheck += len(saviourMoves)

  #print(legalMovesToPreventCheck)
  #print(numOfLegalMovesToPreventCheck)
  return numOfLegalMovesToPreventCheck == 0

def isCheck(thePiece):
  numberOfInstancesOfCheck = 0
  sameColorPiecesDictionary = {}
  tList = deepcopy(chessBoardList)
  for rowIndex in range(8):
    for blockIndex in range(8):
      sameColorIndices = ""
      if (tList[rowIndex][blockIndex])[0] == thePiece[0]:
        sameColorIndices = str(rowIndex) + " " + str(blockIndex)
        sameColorPiecesDictionary.update({sameColorIndices:tList[rowIndex][blockIndex]})

  for sameColorPieceIndexes in sameColorPiecesDictionary.keys():
    indexesNeeded = sameColorPieceIndexes.split()
    rowIndex = int(indexesNeeded[0])
    blockIndex = int(indexesNeeded[1])
    getPossibleMoves(rowIndex, blockIndex, sameColorPiecesDictionary[sameColorPieceIndexes], tList)
    for rowNumber in range(8):
      for blockNumber in range(8):
        if (tList[rowNumber][blockNumber])[0] != thePiece[0] and 'kl' in tList[rowNumber][blockNumber]:
          #print("The killer piece is "+sameColorPiecesDictionary[sameColorPieceIndexes])
          numberOfInstancesOfCheck += 1

    for rowNumber in range(8):
      for blockNumber in range(8):
        if 'l' in tList[rowNumber][blockNumber]:
          block = tList[rowNumber][blockNumber]
          tList[rowNumber][blockNumber] = block[0:int(len(block) - 1)]

  return numberOfInstancesOfCheck != 0

def filterLegalMoves(pRow, pBlock, thePiece, theList):
  #print("Here is the list before filtering. Therefore, this contains all unfiltered moves with legal markers: ")
  #print(theList)
  legalMovesRowAndBlockIndexes = []
  illegalMoveIndexes = []
  for rowIndex in range(8):
    for blockIndex in range(8):
      particularLegalMoveRowAndBlockIndex = []
      if 'l' in theList[rowIndex][blockIndex]:
        particularLegalMoveRowAndBlockIndex.append(rowIndex)
        particularLegalMoveRowAndBlockIndex.append(blockIndex)
        legalMovesRowAndBlockIndexes.append(particularLegalMoveRowAndBlockIndex) #storing all legal moves in a 2d list

  for rowIndex in range(8):
    for blockIndex in range(8):
      if 'l' in theList[rowIndex][blockIndex]:
        block = theList[rowIndex][blockIndex]
        theList[rowIndex][blockIndex] = block[0:int(len(block)-1)] #temporarily eliminating all legal markers from the original list (chessBoardList)

  #if thePiece == 'bq':
    #print("hola, black queen calling")
    #print("Initially, these are my legal moves:", legalMovesRowAndBlockIndexes)

  temporaryList = deepcopy(theList) #temporary list will be used to compute illegal moves while keeping the original chessboardList intact
  #print("This is the temporary list before looping for pieces of the opposite color (what we start with): ")
  #print(temporaryList)

  #approach 3:
  for legalMove in legalMovesRowAndBlockIndexes:
    particularIllegalMove = []
    legalRowIndex = legalMove[0]
    legalBlockIndex = legalMove[1]
    #let us assume a particular allegedly legal move has been made:
    pieceToRemove = temporaryList[legalRowIndex][legalBlockIndex]
    temporaryList[legalRowIndex][legalBlockIndex] = thePiece
    temporaryList[pRow][pBlock] = 'e'

    oppColorPiecesDictionary = {}

    for rowIndex in range(8):
      for blockIndex in range(8):
        oppColorPieceIndexes = ''
        if temporaryList[rowIndex][blockIndex] != 'e' and thePiece[0] != (temporaryList[rowIndex][blockIndex])[0]: #if we encounter a piece of the opposite color
          oppColorPiece = temporaryList[rowIndex][blockIndex]
          oppColorPieceIndexes = str(rowIndex) + " " + str(blockIndex)
          oppColorPiecesDictionary.update({oppColorPieceIndexes:oppColorPiece})

    numOfOppColorPieces = 0
    #now, we will go through each and every piece of the opposite color to check if any of these pieces has a legal move that is a threat to our king
    for oppColorIndexes in oppColorPiecesDictionary.keys():
      rowAndBlockIndexes = oppColorIndexes.split()
      numOfOppColorPieces += 1
      rowIndex = int(rowAndBlockIndexes[0])
      blockIndex = int(rowAndBlockIndexes[1])
      #print(rowIndex)
      #print(blockIndex)
      #print(type(rowIndex))
      #print(type(blockIndex))
      particularOppColorPiece = oppColorPiecesDictionary[oppColorIndexes]
      #print(particularOppColorPiece, " is a piece of the opposite color")
      getPossibleMoves(rowIndex, blockIndex, particularOppColorPiece, temporaryList) #getting the legal moves for a particular piece of the opposite color

      #Now, we will check if any of these moves is a threat our king:
      for row in temporaryList:
        if thePiece[0] +'kl' in row:
          particularIllegalMove.append(legalRowIndex)
          particularIllegalMove.append(legalBlockIndex)
          illegalMoveIndexes.append(particularIllegalMove)

      #after the checking has been done, we remove all legal markers from the temporary list
      for rowIndex in range(8):
        for blockIndex in range(8):
          if 'l' in temporaryList[rowIndex][blockIndex]:
            block = temporaryList[rowIndex][blockIndex]
            temporaryList[rowIndex][blockIndex] = block[0:int(len(block)-1)] #starting afresh by removing all legal markers '''

    #now, we reset:
    temporaryList[legalRowIndex][legalBlockIndex] = pieceToRemove
    temporaryList[pRow][pBlock] = thePiece
    #print("No. of pieces of opposite color covered (should be the same for each experimentally legal move): ", numOfOppColorPieces)

  #print("Number of opposite color pieces:", numOfOppColor)

  #print("These are the illegal moves:", illegalMoveIndexes)
  filteredLegalMoves = []

  for legalMoveIndexes in legalMovesRowAndBlockIndexes:
    if legalMoveIndexes not in illegalMoveIndexes:
      filteredLegalMoves.append(legalMoveIndexes)

  #print("Filtered Legal Moves List: ", filteredLegalMoves)

  for rowIndex in range(8):
    for blockIndex in range(8):
      if [rowIndex, blockIndex] in filteredLegalMoves:
        theList[rowIndex][blockIndex] += 'l' #putting legal markers for all the legal moves that have been filtered
  #print("Filtered List: ")
  #print(theList)

def getPossibleMovesForKing(pRow, pBlock, piece, aList):
  operands = [[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]]
  i = 0
  while i < 8:
    rowOperand = operands[i][0]
    blockOperand = operands[i][1]
    startingRow = pRow
    startingBlock = pBlock
    try:
      if i == 0:
        assert startingRow + rowOperand <= 7
      elif i == 1:
        assert startingRow + rowOperand <= 7 and startingBlock + blockOperand <= 7
      elif i == 2:
        assert startingRow + rowOperand <= 7 and startingBlock + blockOperand >= 0
      elif i == 3:
        assert startingRow + rowOperand >= 0
      elif i == 4:
        assert startingRow + rowOperand >= 0 and startingBlock + blockOperand <= 7
      elif i == 5:
        assert startingRow + rowOperand >= 0 and startingBlock + blockOperand >= 0
      elif i == 6:
        assert startingBlock + blockOperand <= 7
      elif i == 7:
        assert startingBlock + blockOperand >= 0
      
      if aList[startingRow + rowOperand][startingBlock + blockOperand] == 'e' or (aList[startingRow + rowOperand][startingBlock + blockOperand])[0] != piece[0]:
        aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
        i+=1
      else:
        i+=1

    except:
      i += 1

  

def getPossibleMovesForQueen(pRow, pBlock, piece, aList):
  operands = [[1,1],[1,-1],[-1,1],[-1,-1],[1,0],[0,1],[-1,0],[0,-1]]
  i = 0
  while i < 8:
    rowOperand = operands[i][0]
    blockOperand = operands[i][1]
    startingRow = pRow
    startingBlock = pBlock
    try:
      errorFreeAssignmentComplete = False
      while not errorFreeAssignmentComplete:
        if i == 0:
          assert startingRow + rowOperand <= 7 and startingBlock + blockOperand <= 7
        elif i == 1:
          assert startingRow + rowOperand <= 7 and startingBlock + blockOperand >= 0
        elif i == 2:
          assert startingRow + rowOperand >= 0 and startingBlock + blockOperand <= 7
        elif i == 3:
          assert startingRow + rowOperand >= 0 and startingBlock + blockOperand >= 0
        elif i == 4:
          assert startingRow + rowOperand <= 7
        elif i == 5:
          assert startingBlock + blockOperand <= 7
        elif i == 6:
          assert startingRow + rowOperand >= 0
        elif i == 7:
          assert startingBlock + blockOperand >= 0
        
        if aList[startingRow + rowOperand][startingBlock + blockOperand] == 'e':
          aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
          startingRow += rowOperand
          startingBlock += blockOperand
        elif (aList[startingRow + rowOperand][startingBlock + blockOperand])[0] != piece[0]:
          aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
          errorFreeAssignmentComplete = True
          i+=1
          break
        else:
          errorFreeAssignmentComplete = True
          i+=1
          break
        
    except:
      i += 1


def getPossibleMovesForRook(pRow, pBlock, piece, aList):
  operands = [[1,0],[0,1], [-1,0], [0,-1]]
  i = 0
  while i < 4:
    rowOperand = operands[i][0]
    blockOperand = operands[i][1]
    startingRow = pRow
    startingBlock = pBlock
    try:
      errorFreeAssignmentComplete = False
      while not errorFreeAssignmentComplete:
        if i == 0:
          assert startingRow + rowOperand <= 7
        elif i == 1:
          assert startingBlock + blockOperand <= 7
        elif i == 2:
          assert startingRow + rowOperand >= 0
        elif i == 3:
          assert startingBlock + blockOperand >= 0
        
        if aList[startingRow + rowOperand][startingBlock + blockOperand] == 'e':
          aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
          startingRow += rowOperand
          startingBlock += blockOperand
        elif (aList[startingRow + rowOperand][startingBlock + blockOperand])[0] != piece[0]:
          aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
          errorFreeAssignmentComplete = True
          i+=1
          break
        else:
          errorFreeAssignmentComplete = True
          i+=1
          break
        
    except:
      i += 1

        
def getPossibleMovesForBishop(pRow, pBlock, piece, aList):
  operands = [[1,1],[1,-1],[-1,1],[-1,-1]]
  i = 0
  while i < 4:
    rowOperand = operands[i][0]
    blockOperand = operands[i][1]
    startingRow = pRow
    startingBlock = pBlock
    try:
      errorFreeAssignmentComplete = False
      while not errorFreeAssignmentComplete:
        if i == 0:
          assert startingRow + rowOperand <= 7 and startingBlock + blockOperand <= 7
        elif i == 1:
          assert startingRow + rowOperand <= 7 and startingBlock + blockOperand >= 0
        elif i == 2:
          assert startingRow + rowOperand >= 0 and startingBlock + blockOperand <= 7
        elif i == 3:
          assert startingRow + rowOperand >= 0 and startingBlock + blockOperand >= 0
      
        if aList[startingRow + rowOperand][startingBlock + blockOperand] == 'e':
          aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
          startingRow += rowOperand
          startingBlock += blockOperand
        elif (aList[startingRow + rowOperand][startingBlock + blockOperand])[0] != piece[0]:
          aList[startingRow + rowOperand][startingBlock + blockOperand] += 'l'
          errorFreeAssignmentComplete = True
          i+=1
          break
        else:
          errorFreeAssignmentComplete = True
          i+=1
          break
        
    except:
      i += 1


def getPossibleMovesForKnight(pRow, pBlock, piece, aList):
  operands = [[2,1],[2,-1],[1,-2],[-1,-2],[-2,1],[-2,-1],[1,2],[-1,2]]
  errorFreeAssignmentComplete = False
  i = 0
  while not errorFreeAssignmentComplete:
    currentOperandsToUse = operands[i]
    rowOperand = currentOperandsToUse[0]
    blockOperand = currentOperandsToUse[1]
    try:
      assert (pRow + rowOperand >= 0) and (pRow + rowOperand <= 7) and (pBlock + blockOperand >= 0) and (pBlock + blockOperand <= 7)
      if aList[pRow+rowOperand][pBlock+blockOperand] == 'e' or (aList[pRow+rowOperand][pBlock+blockOperand])[0] != piece[0]:
        aList[pRow+rowOperand][pBlock+blockOperand] += 'l'
      i += 1
      if i == 8:
        errorFreeAssignmentComplete = True
        break
    except:
      i += 1
      if i == 8:
        errorFreeAssignmentComplete = True
        break

def getPossibleMovesForPawn(pRow, pBlock, piece, aList):
  if(piece[0] == 'w'):
    if pRow == 1:
      if pBlock == 0:
        if aList[2][0] == 'e':
          aList[2][0] += 'l'
          if aList[3][0] == 'e':
            aList[3][0] += 'l'
        if (aList[2][1])[0] == 'b':
          aList[2][1] += 'l'

      elif pBlock > 0 and pBlock < 7:
        if aList[2][pBlock] == 'e':
          aList[2][pBlock] += 'l'
          if aList[3][pBlock] == 'e':
            aList[3][pBlock] += 'l'
        if (aList[2][pBlock - 1])[0] == 'b':
          aList[2][pBlock - 1] += 'l'
        if (aList[2][pBlock + 1])[0] == 'b':
          aList[2][pBlock + 1] += 'l'
      
      elif pBlock == 7:
        if aList[2][7] == 'e':
          aList[2][7] += 'l'
          if aList[3][7] == 'e':
            aList[3][7] += 'l'
        if (aList[2][6])[0] == 'b':
          aList[2][6] += 'l'
      
    elif pRow > 1:
      if pBlock == 0:
        if aList[pRow+1][0] == 'e':
          aList[pRow+1][0] += 'l'
        if (aList[pRow+1][1])[0] == 'b':
          aList[pRow+1][1] += 'l'

      elif pBlock > 0 and pBlock < 7:
        if aList[pRow+1][pBlock] == 'e':
          aList[pRow+1][pBlock] += 'l'
        if (aList[pRow+1][pBlock-1])[0] == 'b':
          aList[pRow+1][pBlock-1] += 'l'
        if (aList[pRow+1][pBlock+1])[0] == 'b':
          aList[pRow+1][pBlock+1] += 'l'

      elif pBlock == 7:
        if aList[pRow+1][7] == 'e':
          aList[pRow+1][7] += 'l'
        if (aList[pRow+1][6])[0] == 'b':
          aList[pRow+1][6] += 'l'

  elif piece[0] == 'b':
    if pRow == 6:
      if pBlock == 0:
        if aList[5][0] == 'e':
          aList[5][0] += 'l'
          if aList[4][0] == 'e':
            aList[4][0] += 'l'
        if (aList[5][1])[0] == 'w':
          aList[5][1] += 'l'

      elif pBlock > 0 and pBlock < 7:
        if aList[5][pBlock] == 'e':
          aList[5][pBlock] += 'l'
          if aList[4][pBlock] == 'e':
            aList[4][pBlock] += 'l'
        if (aList[5][pBlock - 1])[0] == 'w':
          aList[5][pBlock - 1] += 'l'
        if (aList[5][pBlock + 1])[0] == 'w':
          aList[5][pBlock + 1] += 'l'
      
      elif pBlock == 7:
        if aList[5][7] == 'e':
          aList[5][7] += 'l'
          if aList[4][7] == 'e':
            aList[4][7] += 'l'
        if (aList[5][6])[0] == 'w':
          aList[5][6] += 'l'
      
    elif pRow < 6:
      if pBlock == 0:
        if aList[pRow-1][0] == 'e':
          aList[pRow-1][0] += 'l'
        if (aList[pRow-1][1])[0] == 'w':
          aList[pRow-1][1] += 'l'

      elif pBlock > 0 and pBlock < 7:
        if aList[pRow-1][pBlock] == 'e':
          aList[pRow-1][pBlock] += 'l'
        if (aList[pRow-1][pBlock-1])[0] == 'w':
          aList[pRow-1][pBlock-1] += 'l'
        if (aList[pRow-1][pBlock+1])[0] == 'w':
          aList[pRow-1][pBlock+1] += 'l'

      elif pBlock == 7:
        if aList[pRow-1][7] == 'e':
          aList[pRow-1][7] += 'l'
        if (aList[pRow-1][6])[0] == 'w':
          aList[pRow-1][6] += 'l'

def getPossibleMoves(pieceRow, pieceBlock, thePiece, theList):
  if thePiece[1:] == 'p':
    getPossibleMovesForPawn(pieceRow, pieceBlock, thePiece, theList)
  elif thePiece[1:] == 'n':
    getPossibleMovesForKnight(pieceRow, pieceBlock, thePiece, theList)
  elif thePiece[1:] == 'b':
    getPossibleMovesForBishop(pieceRow, pieceBlock, thePiece, theList)
  elif thePiece[1:] == 'r':
    getPossibleMovesForRook(pieceRow, pieceBlock, thePiece, theList)
  elif thePiece[1:] == 'q':
    getPossibleMovesForQueen(pieceRow, pieceBlock, thePiece, theList)
  elif thePiece[1:] == 'k':
    getPossibleMovesForKing(pieceRow, pieceBlock, thePiece, theList)


def drawBoard():
  gameWin = GraphWin("Chess Window", 400, 400)
  gameWin.setCoords(0, 0, 400, 400)
  yLL = 40
  yUR = 80
  for rowNum in range(1,9):
    xLL = 40
    xUR = 80
    for blockNum in range(1,9):
      if rowNum%2 == 1:
        if blockNum%2 ==1:
          block = Rectangle(Point(xLL, yLL), Point(xUR, yUR))
          block.setFill("brown")
          block.draw(gameWin)
        else:
          block = Rectangle(Point(xLL, yLL), Point(xUR, yUR))
          block.setFill("white")
          block.draw(gameWin)
        if rowNum == 1:
          if blockNum == 1 or blockNum == 8:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u2656")           
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 2 or blockNum == 7:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u2658")      
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 3 or blockNum == 6:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u2657")            
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 4:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u2655")            
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 5:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u2654")          
            piece.setSize(30)
            piece.draw(gameWin)
        elif rowNum == 7:
          piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u265F")
          piece.setSize(30)
          piece.draw(gameWin)
      else:
        if blockNum%2 ==1:
          block = Rectangle(Point(xLL, yLL), Point(xUR, yUR))
          block.setFill("white")
          block.draw(gameWin)
        else:
          block = Rectangle(Point(xLL, yLL), Point(xUR, yUR))
          block.setFill("brown")
          block.draw(gameWin)
        if rowNum == 2:
          piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u2659")          
          piece.setSize(30)
          piece.draw(gameWin)
        elif rowNum == 8:
          if blockNum == 1 or blockNum == 8:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u265C")
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 2 or blockNum == 7:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u265E")
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 3 or blockNum == 6:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u265D")
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 4:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u265B")
            piece.setSize(30)
            piece.draw(gameWin)
          elif blockNum == 5:
            piece = Text(Point((xLL+xUR)/2, (yLL+yUR)/2), u"\u265A")
            piece.setSize(30)
            piece.draw(gameWin)

      xLL += 40
      xUR += 40
    
    yLL += 40
    yUR += 40

  return gameWin

def isLegalMove(destinationX, destinationY, destinationRow, destinationBlock):
  if destinationX < 40 or destinationX > 360 or destinationY < 40 or destinationY > 360:
    print("You clicked outside the board.")
    return False  
  else:
    return 'l' in chessBoardList[destinationRow][destinationBlock]

def cleanUpAfterMakingMove(gWin):
  for rowIndex in range(0,8):
    for blockIndex in range(0,8):
      blockElement = chessBoardList[rowIndex][blockIndex]
      if 'l' in blockElement:
        chessBoardList[rowIndex][blockIndex] = blockElement[0:int(len(blockElement)-1)]
        untouchedBoxXLL = (blockIndex + 1) * 40
        untouchedBoxXUR = untouchedBoxXLL + 40
        untouchedBoxYLL = (rowIndex + 1) * 40
        untouchedBoxYUR = untouchedBoxYLL + 40
        if 'e' in chessBoardList[rowIndex][blockIndex]:
          if (rowIndex + blockIndex) % 2 == 0:
            color = "brown"
          else:
            color = "white"
          emptyBox = Rectangle(Point(untouchedBoxXLL, untouchedBoxYLL), Point(untouchedBoxXUR, untouchedBoxYUR))
          emptyBox.setFill(color)
          emptyBox.draw(gWin)
        else:
          unkilledPieceText = chessBoardList[rowIndex][blockIndex]
          unkilledPieceUnicode = pieceUnicodes[unkilledPieceText]
          unkilledPiece = Text(Point((untouchedBoxXLL + untouchedBoxXUR)/2,(untouchedBoxYLL + untouchedBoxYUR)/2), unkilledPieceUnicode)
          unkilledPiece.setSize(30)
          unkilledPiece.draw(gWin)

def makeMove(gWin, player, alternateXVal, alternateYVal, alternateRowIndex, alternateBlockIndex, whiteKingHasNotMoved, blackKingHasNotMoved, leftWhiteRookHasNotMoved, rightWhiteRookHasNotMoved, leftBlackRookHasNotMoved, rightBlackRookHasNotMoved, enPassantEndangered = {}, enPassantKillers = {}):
  #print("List before making move: ")
  #print(chessBoardList)
  #calculating the current positions of pawns for en-passant
  sameColorPawnPositions = {}
  for rowNum in range(8):
    for blockNum in range(8):
      scPawnIndexes = ""
      if chessBoardList[rowNum][blockNum] == player[0].lower() + 'p':
        scPawnIndexes = str(rowNum) + " " + str(blockNum)
        sameColorPawnPositions.update({scPawnIndexes:chessBoardList[rowNum][blockNum]})

  #print("Pawn positions of player, ", player, ": ", sameColorPawnPositions)


  validMove = False
  while not validMove:    
    if alternateXVal == 1000:  
      print(player+"'s move now")
      userInitialBlock = gWin.getMouse()
      userInitialXVal = userInitialBlock.getX()
      userInitialYVal = userInitialBlock.getY()
    else:
      userInitialXVal = alternateXVal
      userInitialYVal = alternateYVal      
    if userInitialXVal < 40 or userInitialXVal > 360 or userInitialYVal < 40 or userInitialYVal > 360:
      print("You clicked outside the board. Please try again.")
    else:
      userInitialXLL = userInitialXVal - (userInitialXVal % 40)
      userInitialYLL = userInitialYVal - (userInitialYVal % 40)        
      userInitialXUR = userInitialXLL + 40
      userInitialYUR = userInitialYLL + 40
      userInitialRowIndex = int((userInitialYVal // 40) - 1)
      userInitialBlockIndex = int((userInitialXVal // 40) - 1)
      chosenPieceText = chessBoardList[userInitialRowIndex][userInitialBlockIndex]
      if chosenPieceText == 'e':
        print(player+" selected an empty block. Invalid.")
      elif player[0].lower() != chosenPieceText[0]:
        print(player+" chose their opponents piece. Invalid.")
      else:
        getPossibleMoves(userInitialRowIndex, userInitialBlockIndex, chosenPieceText, chessBoardList)
        filterLegalMoves(userInitialRowIndex, userInitialBlockIndex, chosenPieceText, chessBoardList)
        #if chosenPieceText == 'wk':
          #print("List with legal moves marked: ")
          #print(chessBoardList)

        #adding provisions for white to castle:
        if chosenPieceText == 'wk':
          #print("You chose the white king")
          if whiteKingHasNotMoved:
            #print("I recognize that the white king has not moved")
            if not isCheck('b'):
              #print("I recognize that the white king is not currently under check")
              #print("After we check for check, this list should have all legal markers: ")
              #print(chessBoardList)
              if (chessBoardList[0][3] == 'el' and chessBoardList[0][2] == 'e' and chessBoardList[0][1] == 'e') or (chessBoardList[0][5] == 'el' and chessBoardList[0][6] == 'e'):
                #print("I recognize that the white king has empty blocks between itself and either of its rooks")
                if (chessBoardList[0][3] == 'el' and chessBoardList[0][2] == 'e' and chessBoardList[0][1] == 'e'):
                  #print("The left side is empty for queenside castle")
                  if leftWhiteRookHasNotMoved:
                    #print("I recognize that the left side white rook has not moved")
                    chessBoardList[0][4] = 'e'
                    chessBoardList[0][2] = 'wk'
                    if not isCheck('b'):
                      #print("I recognize that the king will be safe on moving.  Therefore castling is legal")
                      chessBoardList[0][2] = 'el'
                      chessBoardList[0][4] = 'wk'
                    else:
                      #print("Can't castle, sorry")
                      chessBoardList[0][2] = 'e'
                      chessBoardList[0][4] = 'wk'
                if (chessBoardList[0][5] == 'el' and chessBoardList[0][6] == 'e'):
                  #print("the right side is empty for king side castle")
                  if rightWhiteRookHasNotMoved:
                    #print("the right side rook has not moved")
                    chessBoardList[0][4] = 'e'
                    chessBoardList[0][6] = 'wk'
                    if not isCheck('b'):
                      #print("I recognize that the king will be safe on moving 2 blocks. therefore castling is legal")
                      chessBoardList[0][6] = 'el'
                      chessBoardList[0][4] = 'wk'
                    else:
                      #print("Can't castle, sorry!")
                      chessBoardList[0][6] = 'e'
                      chessBoardList[0][4] = 'wk'

        #adding provisions for black to castle
        elif chosenPieceText == 'bk':
          if blackKingHasNotMoved:
            if not isCheck('w'):
              if (chessBoardList[7][3] == 'el' and chessBoardList[7][2] == 'e' and chessBoardList[7][1] == 'e') or (chessBoardList[7][5] == 'el' and chessBoardList[7][6] == 'e'):
                if (chessBoardList[7][3] == 'el' and chessBoardList[7][2] == 'e' and chessBoardList[7][1] == 'e'):
                  if leftBlackRookHasNotMoved:
                    chessBoardList[7][4] = 'e'
                    chessBoardList[7][2] = 'bk'
                    if not isCheck('w'):
                      chessBoardList[7][2] = 'el'
                      chessBoardList[7][4] = 'bk'
                    else:
                      chessBoardList[7][2] = 'e'
                      chessBoardList[7][4] = 'bk'
                if (chessBoardList[7][5] == 'el' and chessBoardList[7][6] == 'e'):
                  if rightBlackRookHasNotMoved:
                    chessBoardList[7][4] = 'e'
                    chessBoardList[7][6] = 'bk'
                    if not isCheck('w'):
                      chessBoardList[7][6] = 'el'
                      chessBoardList[7][4] = 'bk'
                    else:
                      chessBoardList[7][6] = 'e'
                      chessBoardList[7][4] = 'bk'

        elif 'p' in chosenPieceText:
          if len(enPassantEndangered) == 1:
            checkingString = str(userInitialRowIndex) + " " + str(userInitialBlockIndex)
            if checkingString in enPassantKillers.keys():
              if chosenPieceText == 'wp':
                endangeredPawnRowIndex = (enPassantEndangered['bp'])[0]
                endangeredPawnBlockIndex = (enPassantEndangered['bp'])[1]
                if chessBoardList[endangeredPawnRowIndex + 1][endangeredPawnBlockIndex] == 'e':
                  chessBoardList[endangeredPawnRowIndex][endangeredPawnBlockIndex] = 'e'
                  chessBoardList[endangeredPawnRowIndex + 1][endangeredPawnBlockIndex] = 'wp'
                  chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'e'
                  if not isCheck('b'):
                    chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'wp'
                    chessBoardList[endangeredPawnRowIndex][endangeredPawnBlockIndex] = 'bp'
                    chessBoardList[endangeredPawnRowIndex + 1][endangeredPawnBlockIndex] = 'el'
                  else:
                    chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'wp'
                    chessBoardList[endangeredPawnRowIndex][endangeredPawnBlockIndex] = 'bp'
                    chessBoardList[endangeredPawnRowIndex + 1][endangeredPawnBlockIndex] = 'e'

              if chosenPieceText == 'bp':
                endangeredPawnRowIndex = (enPassantEndangered['wp'])[0]
                endangeredPawnBlockIndex = (enPassantEndangered['wp'])[1]
                if chessBoardList[endangeredPawnRowIndex - 1][endangeredPawnBlockIndex] == 'e':
                  chessBoardList[endangeredPawnRowIndex][endangeredPawnBlockIndex] = 'e'
                  chessBoardList[endangeredPawnRowIndex - 1][endangeredPawnBlockIndex] = 'bp'
                  chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'e'
                  if not isCheck('w'):
                    chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'bp'
                    chessBoardList[endangeredPawnRowIndex][endangeredPawnBlockIndex] = 'wp'
                    chessBoardList[endangeredPawnRowIndex - 1][endangeredPawnBlockIndex] = 'el'
                  else:
                    chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'bp'
                    chessBoardList[endangeredPawnRowIndex][endangeredPawnBlockIndex] = 'wp'
                    chessBoardList[endangeredPawnRowIndex + 1][endangeredPawnBlockIndex] = 'e'

        showLegalMoves(gWin)
        #print("List with legal moves marked: ")
        #print(chessBoardList)

        userFinalBlock = gWin.getMouse()
        userFinalXVal = userFinalBlock.getX()
        userFinalYVal = userFinalBlock.getY()
        userFinalRowIndex = int((userFinalYVal // 40) - 1)
        userFinalBlockIndex = int((userFinalXVal // 40) - 1)
        if player[0].lower() == (chessBoardList[userFinalRowIndex][userFinalBlockIndex])[0]:
          cleanUpAfterMakingMove(gWin)
          #print("As we are testing what happens if player decides to move a different piece after making its initial choice, we must clean the list before recursively calling the function. Thus, this list should have no legal markers: ")
          #print(chessBoardList)
          validMove = True
          makeMove(gWin, player, userFinalXVal, userFinalYVal, userFinalRowIndex, userFinalBlockIndex, whiteKingHasNotMoved, blackKingHasNotMoved, leftWhiteRookHasNotMoved, rightWhiteRookHasNotMoved, leftBlackRookHasNotMoved, rightBlackRookHasNotMoved, enPassantEndangered, enPassantKillers)

        elif isLegalMove(userFinalXVal, userFinalYVal, userFinalRowIndex, userFinalBlockIndex):
          userFinalXLL = userFinalXVal - (userFinalXVal % 40)
          userFinalYLL = userFinalYVal - (userFinalYVal % 40)
          userFinalXUR = userFinalXLL + 40
          userFinalYUR = userFinalYLL + 40

          #discussing pawn promotion:
          if (userFinalRowIndex == 7 or userFinalRowIndex == 0) and 'p' in chosenPieceText:
            chosenPieceText = player[0].lower() + 'q'
            chessBoardList[userFinalRowIndex][userFinalBlockIndex] = chosenPieceText
          else:
            chessBoardList[userFinalRowIndex][userFinalBlockIndex] = chosenPieceText

          #discussing castling:
          if (chosenPieceText == 'wk'):
            if (userFinalBlockIndex - userInitialBlockIndex == -2):
              chessBoardList[0][0] = 'e'
              chessBoardList[0][3] = 'wr'
              whiteRookUnicode = pieceUnicodes['wr']
              emptyBlock = Rectangle(Point(40, 40), Point(80,80))
              emptyBlock.setFill("brown")
              emptyBlock.draw(gWin)
              whiteRookNewBlock = Rectangle(Point(160, 40), Point(200, 80))
              whiteRookNewBlock.setFill("white")
              whiteRookNewBlock.draw(gWin)
              whiteRookDrawing = Text(Point(180, 60), whiteRookUnicode)
              whiteRookDrawing.setSize(30)
              whiteRookDrawing.draw(gWin)
            elif (userFinalBlockIndex - userInitialBlockIndex == 2):
              chessBoardList[0][7] = 'e'
              chessBoardList[0][5] = 'wr'
              whiteRookUnicode = pieceUnicodes['wr']
              emptyBlock = Rectangle(Point(320, 40), Point(360,80))
              emptyBlock.setFill("white")
              emptyBlock.draw(gWin)
              whiteRookNewBlock = Rectangle(Point(240, 40), Point(280, 80))
              whiteRookNewBlock.setFill("white")
              whiteRookNewBlock.draw(gWin)
              whiteRookDrawing = Text(Point(260, 60), whiteRookUnicode)
              whiteRookDrawing.setSize(30)
              whiteRookDrawing.draw(gWin)
          elif (chosenPieceText == 'bk'):
            if (userFinalBlockIndex - userInitialBlockIndex == -2):
              chessBoardList[7][0] = 'e'
              chessBoardList[7][3] = 'br'
              blackRookUnicode = pieceUnicodes['br']
              emptyBlock = Rectangle(Point(40, 320), Point(80,360))       
              emptyBlock.setFill("white")
              emptyBlock.draw(gWin)
              blackRookNewBlock = Rectangle(Point(160, 320), Point(200, 360))
              blackRookNewBlock.setFill("brown")
              blackRookNewBlock.draw(gWin)
              blackRookDrawing = Text(Point(180, 340), blackRookUnicode)
              blackRookDrawing.setSize(30)
              blackRookDrawing.draw(gWin)
            elif (userFinalBlockIndex - userInitialBlockIndex == 2):
              chessBoardList[7][7] = 'e'
              chessBoardList[7][5] = 'br'
              blackRookUnicode = pieceUnicodes['br']
              emptyBlock = Rectangle(Point(320, 320), Point(360,360))
              emptyBlock.setFill("brown")
              emptyBlock.draw(gWin)
              blackRookNewBlock = Rectangle(Point(240, 320), Point(280, 360))
              blackRookNewBlock.setFill("brown")
              blackRookNewBlock.draw(gWin)
              blackRookDrawing = Text(Point(260, 340), blackRookUnicode)
              blackRookDrawing.setSize(30)
              blackRookDrawing.draw(gWin)

          #discussing en-passant
          if str(userInitialRowIndex) + " " + str(userInitialBlockIndex) in enPassantKillers.keys():
            if chosenPieceText == 'wp':
              if userFinalRowIndex == (enPassantEndangered['bp'])[0] + 1 and userFinalBlockIndex == (enPassantEndangered['bp'])[1]:
                chessBoardList[(enPassantEndangered['bp'])[0]][(enPassantEndangered['bp'])[1]] = 'e'
                #draw empty box:
                emptyRowIndex = (enPassantEndangered['bp'])[0]
                print(emptyRowIndex)
                emptyBlockIndex = (enPassantEndangered['bp'])[1]
                print(emptyBlockIndex)
                emptyXLL = (emptyBlockIndex + 1) * 40
                emptyXUR = emptyXLL + 40
                emptyYLL = (emptyRowIndex + 1) * 40
                emptyYUR = emptyYLL + 40
                if (emptyRowIndex + emptyBlockIndex) %2 == 0:
                  color = "brown"
                else:
                  color = "white"
                print("drawing empty block now")
                emptyBlock = Rectangle(Point(emptyXLL, emptyYLL), Point(emptyXUR, emptyYUR))
                emptyBlock.setFill(color)
                emptyBlock.draw(gWin)

            elif chosenPieceText == 'bp':
              if userFinalRowIndex == (enPassantEndangered['wp'])[0] - 1 and userFinalBlockIndex == (enPassantEndangered['wp'])[1]:
                chessBoardList[(enPassantEndangered['wp'])[0]][(enPassantEndangered['wp'])[1]] = 'e'
                #draw empty box:
                emptyRowIndex = (enPassantEndangered['wp'])[0]
                emptyBlockIndex = (enPassantEndangered['wp'])[1]
                print(emptyRowIndex)
                print(emptyRowIndex)
                emptyXLL = (emptyBlockIndex + 1) * 40
                emptyXUR = emptyXLL + 40
                emptyYLL = (emptyRowIndex + 1) * 40
                emptyYUR = emptyYLL + 40
                if (emptyRowIndex + emptyBlockIndex) %2 == 0:
                  color = "brown"
                else:
                  color = "white"
                emptyBlock = Rectangle(Point(emptyXLL, emptyYLL), Point(emptyXUR, emptyYUR))
                emptyBlock.setFill(color)
                emptyBlock.draw(gWin)

          chosenPieceUnicode = pieceUnicodes[chosenPieceText]
          if (userFinalRowIndex + userFinalBlockIndex) % 2 == 0:
            color = "brown"
          else:
            color = "white"
          destinationBlock = Rectangle(Point(userFinalXLL, userFinalYLL), Point(userFinalXUR, userFinalYUR))
          destinationBlock.setFill(color)
          destinationBlock.draw(gWin)
          pieceImage = Text(Point((userFinalXLL + userFinalXUR)/2, (userFinalYLL + userFinalYUR)/2), chosenPieceUnicode)
          pieceImage.setSize(30)
          pieceImage.draw(gWin)

          chessBoardList[userInitialRowIndex][userInitialBlockIndex] = 'e' #must do this on the condition that the player has made a legal move
          if (userInitialRowIndex + userInitialBlockIndex) % 2 == 0:
            color = "brown"
          else:
            color = "white"
          emptyImage = Rectangle(Point(userInitialXLL, userInitialYLL), Point(userInitialXUR, userInitialYUR))
          emptyImage.setFill(color)
          emptyImage.draw(gWin)
          cleanUpAfterMakingMove(gWin)
          #print("Cleaned list: ")
          #print(chessBoardList)

          if (isCheck(chosenPieceText) and chosenPieceText[0] == 'w'):
            print("Black is under check!")
          elif (isCheck(chosenPieceText) and chosenPieceText[0] == 'b'):
            print("White is under check!")

          validMove = True
          
        else:
          print("Invalid Move. Please try again.")
          cleanUpAfterMakingMove(gWin)
          alternateXVal = 1000
          #print("Chessboard list after player made an illegal move: (should have no l markers) ")
          #print(chessBoardList)

  #print("Cleaned list after making move: ")
  #print(chessBoardList)
  if chessBoardList[0][4] != 'wk':
    whiteKingHasNotMoved = False
  if chessBoardList[7][4] != 'bk':
    blackKingHasNotMoved = False
  if chessBoardList[0][4] != 'wk' and chessBoardList[0][0] !='wr':
    whiteKingHasNotMoved = False
    leftWhiteRookHasNotMoved = False
  if chessBoardList[0][4] != 'wk' and chessBoardList[0][7] !='wr':
    whiteKingHasNotMoved = False
    rightWhiteRookHasNotMoved = False
  if chessBoardList[7][4] != 'bk' and chessBoardList[7][0] != 'br':
    blackKingHasNotMoved = False
    leftBlackRookHasNotMoved = False
  if chessBoardList[7][4] != 'bk' and chessBoardList[7][7] != 'br':
    blackKingHasNotMoved = False
    rightBlackRookHasNotMoved = False
  if chessBoardList[0][0] != 'wr':
    leftWhiteRookHasNotMoved = False
  if chessBoardList[0][7] != 'wr':
    rightWhiteRookHasNotMoved = False
  if chessBoardList[7][0] != 'br':
    leftBlackRookHasNotMoved = False
  if chessBoardList[7][7] != 'br':
    rightBlackRookHasNotMoved = False

  enPassantEndangeredPieceIndexes = []
  enPassantEndangered = {}
  enPassantKillers = {}
  #checking for en Passant:
  #if white is in danger of en passant
  #print("About to count pieces in danger of en-passant: ")
  for rowNum in range(8):
    for blockNum in range(8):
      if chessBoardList[rowNum][blockNum] == player[0].lower() + 'p':
        if player == 'White':
          stringToCheck = str(rowNum - 2) + " " + str(blockNum)
          if stringToCheck in sameColorPawnPositions.keys():
            enPassantEndangeredPieceIndexes.append(rowNum)
            enPassantEndangeredPieceIndexes.append(blockNum)
            enPassantEndangered.update({chessBoardList[rowNum][blockNum]:enPassantEndangeredPieceIndexes})
            for concernedBlockNum in range(8):
              enPassantKillerPieceIndexes = ""
              if concernedBlockNum == blockNum - 1 or concernedBlockNum == blockNum + 1:
                if chessBoardList[rowNum][concernedBlockNum] == 'bp':
                  enPassantKillerPieceIndexes = str(rowNum) + " " + str(concernedBlockNum)
                  enPassantKillers.update({enPassantKillerPieceIndexes:chessBoardList[rowNum][concernedBlockNum]})

        elif player == "Black":
          stringToCheck = str(rowNum + 2) + " " + str(blockNum)
          if stringToCheck in sameColorPawnPositions.keys():
            enPassantEndangeredPieceIndexes.append(rowNum)
            enPassantEndangeredPieceIndexes.append(blockNum)
            enPassantEndangered.update({chessBoardList[rowNum][blockNum]:enPassantEndangeredPieceIndexes})
            for concernedBlockNum in range(8):
              enPassantKillerPieceIndexes = ""
              if concernedBlockNum == blockNum - 1 or concernedBlockNum == blockNum + 1:
                if chessBoardList[rowNum][concernedBlockNum] == 'wp':
                  enPassantKillerPieceIndexes = str(rowNum) + " " + str(concernedBlockNum)
                  enPassantKillers.update({enPassantKillerPieceIndexes:chessBoardList[rowNum][concernedBlockNum]})

  #print("List after making move. Look out for castling, en-Passant, pawn promotion etc. : ", chessBoardList)

  if player == 'White':
    return ['Black', isCheckMate(chosenPieceText), whiteKingHasNotMoved, blackKingHasNotMoved, leftWhiteRookHasNotMoved, rightWhiteRookHasNotMoved,leftBlackRookHasNotMoved, rightBlackRookHasNotMoved, enPassantEndangered, enPassantKillers]
  elif player == 'Black':
    return ['White', isCheckMate(chosenPieceText), whiteKingHasNotMoved, blackKingHasNotMoved, leftWhiteRookHasNotMoved, rightWhiteRookHasNotMoved,leftBlackRookHasNotMoved, rightBlackRookHasNotMoved, enPassantEndangered, enPassantKillers]


def playGame():
  gameOver = False
  playerColor = 'White'
  gamingWindow = drawBoard()
  wkNotMoved = True
  bkNotMoved = True
  lWRNotMoved = True
  rWRNotMoved = True
  lBRNotMoved = True
  rBRNotMoved = True
  inDangerOfEnPassant = {}
  killerOfEnPassant = {}
  while not gameOver:
    directions = makeMove(gamingWindow, playerColor, 1000, 1000, 1000, 1000, wkNotMoved, bkNotMoved, lWRNotMoved, rWRNotMoved, lBRNotMoved, rBRNotMoved, inDangerOfEnPassant, killerOfEnPassant)

    if directions[0] == 'Black' and directions[1] == True:
      print("Checkmate. White wins!")
      gameOver = directions[1]
    elif directions[0] == 'White' and directions[1] == True:
      print("Checkmate. Black wins!")
      gameOver = directions[1]
    else:
      playerColor = directions[0]
      wkNotMoved = directions[2]
      bkNotMoved = directions[3]
      lWRNotMoved = directions[4]
      rWRNotMoved = directions[5]
      lBRNotMoved = directions[6]
      rBRNotMoved = directions[7]
      inDangerOfEnPassant = directions[8]
      killerOfEnPassant = directions[9]
      #print("After this move: ")
      #print("White King has not moved: ", wkNotMoved)
      #print("Black King has not moved: ", bkNotMoved)
      #print("Left white rook has not moved: ", lWRNotMoved)
      #print("Right white rook has not moved: ", rWRNotMoved)
      #print("Left black rook has not moved: ", lBRNotMoved)
      #print("Right black rook has not moved: ", rBRNotMoved)
      #print("Pieces in danger of en-passant: ", inDangerOfEnPassant)
      #print("Pieces that can kill via en-passant: ", killerOfEnPassant)
      
#Initializing important list/s and dictionary/ies
chessBoardList = [['wr','wn','wb','wq','wk','wb','wn','wr'],['wp','wp','wp','wp','wp','wp','wp','wp'],['e','e','e','e','e','e','e','e'],['e','e','e','e','e','e','e','e'],['e','e','e','e','e','e','e','e'],['e','e','e','e','e','e','e','e'],['bp','bp','bp','bp','bp','bp','bp','bp'],['br','bn','bb','bq','bk','bb','bn','br']]
pieceUnicodes = {'wr': u"\u2656", 'wn': u"\u2658", 'wb': u"\u2657", 'wq': u"\u2655", 'wk': u"\u2654", 'wp': u"\u2659", 'br': u"\u265C", 'bn': u"\u265E", 'bb': u"\u265D", 'bq': u"\u265B", 'bk': u"\u265A", 'bp': u"\u265F"}

playGame()
