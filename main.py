
import cv2
import HandTrakingModule as htm

from time import sleep


# comment

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetector(detectionCon=0.8)

keys = [["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
		["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
		["W", "X", "C", "V", "B", "N", ",", ";", ":"]]

def drawALL(img, buttonList):

	for button in buttonList: 
		x, y = button.pos
		w, h = button.size	
		#cv2.rectangle(img, self.pos, (x+w, y+h),(255, 0, 255), cv2.FILLED)
		cv2.rectangle(img, (button.pos[0], button.pos[1]) , (x+w, y+h), (255,0,255), cv2.FILLED)
		cv2.putText(img, button.text, (x + 25, y + 75), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)	

	return img

class Button():
	def __init__(self, pos, text, size= [85, 85]):
		self.pos = pos
		self.text = text
		self.size = size

		

buttonList = []

finalText = ""
"""
myButton = Button([100, 100], "A")
myButton1 = Button([200, 100], "Z")
myButton2 = Button([300, 100], "E")
"""

for i in range(0,3):
		for j, key in enumerate(keys[i]):
			buttonList.append(Button([100*j+50, 100*i+50], key))

while True:
	success, img = cap.read()
	_ , img = detector.findHands(img)
	lmList = detector.findPosition(img)

	img = drawALL(img, buttonList)

	if lmList:

		for button in buttonList:
			x, y = button.pos
			w, h = button.size
			#print("lmList[8][1]:", lmList[8][1])
			if x < lmList[8][1]< x+w and y< lmList[8][2] < y+h:
				cv2.rectangle(img, (button.pos[0], button.pos[1]), (x+w, y+h), (175, 0, 175), cv2.FILLED)
				cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

				#l, _,_  = detector.findDistance(8, 12, img)
				l, _,_  = detector.findDistance((lmList[8][1], lmList[8][2]), (lmList[12][1], lmList[12][2]), img)
				print(l)
				if l < 30:
					cv2.rectangle(img, (button.pos[0], button.pos[1]), (x+w , y+h), (0, 255, 0), cv2.FILLED)
					cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
					finalText+= button.text
					sleep(0.2)


	cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
	cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)			


	cv2.imshow("Image", img)
	key = cv2.waitKey(1)

	if key == ord('q') or key == ord('Q'):
		break
    	