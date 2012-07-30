import random


def move(lag,log):
    return lag,log
    


def calculate(current,destination):
    #if the bot arrived to the destination
    if current[0] == destination[0] and current[1] == destination[1]:
        return current
    #still moving
    else:
        return current
        
