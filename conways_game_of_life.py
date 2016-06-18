import midi
import time

conn = midi.Connection()

matrix = [[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0]]

while True:
    if conn.poll():
        button = conn.read()
        if button.grid and button.down:
            matrix[button.y][button.x] = 0 if matrix[button.y][button.x] else 1
            led = midi.LED(conn,button.coordinate,127*matrix[button.y][button.x])
            led.send()
        elif button.side:
            break

while True:
    newMatrix = [[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]]
    for y,row in enumerate(matrix):
        for x,val in enumerate(row):
            neighbors = []
            if x > 0:
                neighbors.append(matrix[y][x-1])
            if x < 7:
                neighbors.append(matrix[y][x+1])
            if y > 0:
                neighbors.append(matrix[y-1][x])
            if y < 7:
                neighbors.append(matrix[y+1][x])
            if x > 0 and y > 0:
                neighbors.append(matrix[y-1][x-1])
            if x > 0 and y < 7:
                neighbors.append(matrix[y+1][x-1])
            if x < 7 and y > 0:
                neighbors.append(matrix[y-1][x+1])
            if x < 7 and y < 7:
                neighbors.append(matrix[y+1][x+1])
            aliveNeighbors = 0
            for val in neighbors:
                if val:
                    aliveNeighbors += 1
            if matrix[y][x]:
                if aliveNeighbors < 2:
                    newMatrix[y][x] = 0
                elif aliveNeighbors < 4:
                    newMatrix[y][x] = 1
                else:
                    newMatrix[y][x] = 0
            else:
                if aliveNeighbors == 3:
                    newMatrix[y][x] = 1

    for y,row in enumerate(matrix):
        for x,val in enumerate(row):
            led = midi.LED(conn,(x,y),127*newMatrix[y][x])
            led.send()
    matrix = newMatrix
    
    time.sleep(1)
    
    """if conn.poll():
        button = conn.read()
        if button.side:
            break"""

conn.close()
                
        
