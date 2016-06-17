import pygame.midi as midi
midi.init()
import time
import random

noteOn = 1
noteOff = 0

class Connection:
    def __init__(self):
        infos = [midi.get_device_info(n) for n in range(0, midi.get_count())]
        i=0
        o=0
        for (n,info) in enumerate(infos):
            if info[2] and "Launchpad" in info[1]:
                i=n
            elif info[3] and "Launchpad" in info[1]:
                o=n
        print "Detected Launchpad on input " + str(i) + " and output " + str(o)
        self.input = midi.Input(i)
        self.output = midi.Output(o)
        print "Connection established"

    def poll(self):
        return self.input.poll()

    def read(self,n=1):
        data = self.input.read(n)
        return Button(self,data=data)

    def close(self):
        self.input.close()
        self.output.close()
        midi.quit()


class Button:
    def __init__(self,connection,data):
        self.connection=connection
        self.number = data[0][0][1]
        self.x = self.number%10 - 1
        self.y = self.number/10 - 1
        self.coordinate = (self.x,self.y)
        self.down = data[0][0][2]==127
        self.up = data[0][0][2]!=127

    def send(self):
        data = [[[144, self.number, self.velocity, 0], midi.time()]]
        self.connection.output.write(data)

class LED:
    def __init__(self,connection,coordinate,velocity):
        self.connection=connection
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.velocity = velocity
        self.coordinate = coordinate
        self.number = 10*(self.y+1) + self.x+1
        self.noteOn = self.velocity==127

    def send(self):
        data = [[[144, self.number, self.velocity, 0], midi.time()]]
        self.connection.output.write(data)

    
