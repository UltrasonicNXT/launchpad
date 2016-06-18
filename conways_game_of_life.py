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
    time.sleep(0.001)

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
            left = x-1 if x > 0 else 7
            right = x+1 if x < 7 else 0
            down = y-1 if y > 0 else 7
            up = y+1 if y < 7 else 0

            neighborAddresses = [(left,up),   (x,up),   (right,up),
                                 (left,y),              (right,y),
                                 (left,down), (x,down), (right,down)]
            
            aliveNeighbors = 0
            for coordinate in neighborAddresses:
                if matrix[coordinate[1]][coordinate[0]]:
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
    
    time.sleep(0.1)
    
    if conn.poll():
        button = conn.read()
        if button.side and button.down:
            print "breaking"
            break

conn.close()
                
        
