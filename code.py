import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from pythonosc import udp_client
import argparse


cap = cv2.VideoCapture(0) #0 är den inbyggda kameran. Finns det fler kameror inkopplade byt värde.
detector = FaceMeshDetector(maxFaces=1)


if __name__ == "__main__": 
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port) #clienten skapad med argument ip och port

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False) #Detekterar ansiktet och skapar en lista med x och y värden som motsvarar vart vi är på ansiktet 

    if faces: 
        face = faces[0] 
        pointLeft = face[145] #vänster öga
        pointRight = face[374] #höger öga 
    
        w, _ = detector.findDistance(pointLeft, pointRight) #avstånd i pixlar mellan ögonen
        W = 6.3 # avstånd i cm mellan ögon. Standard män= 64mm, kvinnor= 62mm.

        
        # Hitta focal length och distans 
        f = 840 #f=(w*d)/W. Beräknades genom att mäta ansiktet 50cm från kameran 
        d = int((W * f) / w) #använder det standardiserade f:et för att hitta alla distanser. 

        print(d)
        client.send_message("/localhost",d) #Skickar till MISK
        cvzone.putTextRect(img, f'Distance: {int(d)}cm',
                           (face[10][0] - 200, face[10][1] - 50), #placering av textrutan i fönstret. [10]=pannan
                           scale=2, colorR=(30, 132, 73), font=5)

    
    cv2.imshow("Image", img) #öppna fönster med kameran. Kan bara kommenteras bort om det inte önskas.
    cv2.waitKey(1) #stänger fönstret med ´ 
