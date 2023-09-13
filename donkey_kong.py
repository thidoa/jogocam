import cv2
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

z_press = False
a_press  = False
right_press = False
down_press = False
left_press = False

agacha_line = 250
pula_line = 50
#100
andar_line = 100

video = cv2.VideoCapture(0)

def draw_quare(frame, x, y, size, color):
    cv2.rectangle(frame, (x, y), (x + size, y + size), color, thickness=2)
    
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while video.isOpened():
    success, image = video.read()

    image = cv2.flip(image, 1)

    if not success:
      print("Ignoring empty camera frame.")
      continue

    
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())


    if results.pose_landmarks:
        h, w, p = image.shape
      
        # print(h, w)

        cv2.line(image, (0, pula_line), (w, pula_line), (0, 0, 255), 2)
        cv2.putText(image, 'PULAR', (290, pula_line - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)

        #                      x    y     x   y
        cv2.rectangle(image, (500, 100), (w, 247), (0, 255, 0), thickness=2)
        cv2.putText(image, 'FRENTE', (540, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
        
        #                     x   y      x    y
        cv2.rectangle(image, (0, 100), (150, 247), (0, 102, 255), thickness=2)
        cv2.putText(image, 'TRAS', (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,102,255),2)

        #                      x    y      x    y
        cv2.rectangle(image, (245, 270), (395, 417), (130, 0, 70), thickness=2)
        cv2.putText(image, 'ROLAR', (295, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (130,0,70),2)


        cv2.line(image, (0, agacha_line), (w, agacha_line), (255, 0, 0), 2)
        cv2.putText(image, 'AGACHAR', (290, (agacha_line + 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2)

        pontos = []
        for id, cord in enumerate(results.pose_landmarks.landmark):
            cx, cy, cz = int(cord.x*w), int(cord.y*h), int(cord.z*p)
            cv2.putText(image, str(id), (cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2, cv2.LINE_AA)
            pontos.append((cx, cy, cz))

        # PULAR
        if pontos[4][1] < pula_line:
            if z_press == False:
                pyautogui.keyDown('z')
                z_press = True
        else:
            if z_press:
                pyautogui.keyUp('z')
                z_press = False

        # ABAIXAR
        if pontos[4][1] > agacha_line:
            if down_press == False:
                pyautogui.keyDown('down')
                down_press = True
        else:
            if down_press:
                pyautogui.keyUp('down')
                down_press = False

        # FRENTE
        if (pontos[19][0] > 500 and pontos[19][0] < 640) and (pontos[19][1] > 100 and pontos[19][1] < 247):
            if right_press == False:
                pyautogui.keyDown('right')
                right_press = True
        else:
            if right_press:
                pyautogui.keyUp('right')
                right_press = False
        
        # TRAS
        if (pontos[20][0] > 0 and pontos[20][0] < 150) and (pontos[20][1] > 100 and pontos[20][1] < 247):
            if left_press == False:
                pyautogui.keyDown('left')
                left_press = True
        else:
            if left_press:
                pyautogui.keyUp('left')
                left_press = False

        # ROLAR
        if ((pontos[20][0] > 245 and pontos[20][0] < 295) and (pontos[20][1] > 270 and pontos[20][1] < 417)) or ((pontos[19][0] > 245 and pontos[19][0] < 395) and (pontos[19][1] > 270 and pontos[19][1] < 417)):
            if a_press == False:
                pyautogui.keyDown('a')
                a_press = True
        else:
            if a_press:
                pyautogui.keyUp('a')
                a_press = False


    cv2.imshow('THIAGO', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
video.release()