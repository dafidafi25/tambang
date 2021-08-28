from smartCard2 import DetectReader,smartCard
from time import sleep

while len(DetectReader()) == 0:
    print("Trying to detect reader")
    sleep(1)


while(True):
    sleep(1)