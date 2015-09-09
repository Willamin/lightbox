#!/usr/local/bin/python
import sys, tty, termios


class LightBox: 
	lights = [ 
		-1,
		True, True,
		True, True,
		True, True
	]
	pins = [
		-1,
		4, 17,
		22, 23,
		24, 25
	]

def setupPins(box):
	if dryrun:
		return
	GPIO.setmode(GPIO.BCM)
	for i in range(1,len(box.pins)):
		GPIO.setup(box.pins[i], GPIO.OUT)


def refresh (box):
	if dryrun:
		return
	print "Refreshing lights"
	for i in range(1,len(box.lights)):
		GPIO.output(box.pins[i],box.lights[i])

def list(box):
	r = ''
	for i in range(1,len(box.lights)):
		value = box.lights[i]
		r += str(i)
		r += ':'
		r += str(value)
		if i % 2 == 0:
			r += "\n"
		else:
			r += "   "
	return r

def loop(box):
	c = getChar()
	if c == 'q':
		return False
	elif c == 'h':
		print help()
	elif c == 'l':
		print list(box)
	elif isInt(c):
		toggleLight(box, c)
		if not dryrun:
			refresh(box)
	return True

def toggleLight(box, c):
	i = int(c)
	if 1 <= i < len(box.lights):
		print 'toggling light', i, "\n  ", box.lights[i], '=>', not box.lights[i]
		box.lights[i] = not box.lights[i]


def help():
	return ("\nLightbox\n"
			"\n[q]: quit"
			"\n[h]: help"
			"\n[l]: list")

def getChar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
	    tty.setraw(sys.stdin.fileno())
	    ch = sys.stdin.read(1)
	finally:
	    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def find(element,list_element):
    try:
        index_element=list_element.index(element)
        return index_element
    except ValueError:
        return -1
		

print 'Hi'
dryrun = False
for arg in sys.argv:
	if arg == '-d':
		dryrun = True

if not dryrun:
	import RPi.GPIO as GPIO


looping = True
box = LightBox()
setupPins(box)
refresh(box)
while looping:
	looping = loop(box)
print 'Bye'