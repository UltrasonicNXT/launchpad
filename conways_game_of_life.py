import midi

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
