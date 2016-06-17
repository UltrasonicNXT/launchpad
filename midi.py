import pygame.midi as midi
midi.init()
import time
import random

noteOn = 1
noteOff = 0

inputConnection = None
outputConnection = None

def begin():
    (inputID,outputID) = deviceInfo();
    print "Detected Launchpad on input " + str(inputID) + " and output " + str(outputID)
    inputConnection = midi.Input(inputID)
    outputConnection = midi.Output(outputID)
    print "Connection established"

def deviceInfo():
    infos = [midi.get_device_info(n) for n in range(0, midi.get_count())]
    i=0
    o=0
    for (n,info) in enumerate(infos):
        if info[2] and "Launchpad" in info[1]:
            i=n
        elif info[3] and "Launchpad" in info[1]:
            o=n
    return (i,o)

class Note:
    def __init__(self,data=None,coordinate=None,velocity=None):
        if data:
            self.velocity = data[0][0][2]
            self.number = data[0][0][1]
            self.x = self.number%10 - 1
            self.y = self.number/10 - 1
            self.coordinate = (self.x,self.y)
        else:
            self.x = coordinate[0]
            self.y = coordinate[1]
            self.velocity = velocity
            self.coordinate = coordinate
            self.number = 10*(y+1) + x+1
        self.noteOn = self.velocity==127

    def send(self):
        data = [[[144, self.number, self.velocity, 0], midi.time()]]
        outputConnection.write(data)

def close():
    inputConnection.close()
    outputConnection.close()
    midi.quit()



    
