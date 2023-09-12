import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
keyboard = Controller()
import pyautogui
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
(screen_width, screen_height) = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]
state = None


# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):
    global state

    if hand_landmarks:
       # Get all the landmarks of the first hand visible
       landmarks = hand_landmarks[handNo].landmark
       fingers = []
       for lm_index in tipIds:
          # Get finger tip and bottom y position
          fingerTipY = landmarks[lm_index].y
          fingerBottomY = landmarks[lm_index-2].y
          #Get ThumbTip and BottomX
          thumbTipX = landmarks[lm_index].x
          thumbBottomX = landmarks[lm_index-2].x
          #Check if any finger is open or closed
          if lm_index!=4:
             if fingerTipY < fingerBottomY:
                fingers.append(1)
                print('Finger With Id', lm_index, 'Is Open')
             if fingerTipY > fingerBottomY:
                fingers.append(0)
                print('Finger With Id', lm_index, 'Is Closed')
          else:
             if thumbTipX > thumbBottomX:
                fingers.append(1)
                print('Thumb is open')
             if thumbTipX < thumbBottomX:
                fingers.append(0)
                print('Thumb is closed')
       totalFingers = fingers.count(1)
       if totalFingers == 4:
          state = 'Play'
       if totalFingers == 0 and state == 'Play':
          state = 'Pause'
          keyboard.press(key.space)
       fingerTipX = (landmarks[8].x)*width
       if totalFingers == 1:
          if fingerTipX < width - 400:
             print('Play backwards')
             keyboard.press(Key.left)
          if fingerTipX > width - 50:
             print('Play forward')
             keyboard.press(Key.right)
             
      
            
              
      
      
       
# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)
    countFingers(image, hand_landmarks  )

    # Get Hand Fingers Position        
    ##################
    # ADD CODE HERE
    ##################

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
