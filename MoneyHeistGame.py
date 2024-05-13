from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


tank = {'x': 400, 'y': 400, 'direction': 'up'}
fireTimer = 100
Bullet = False
Score = 0
fast_travel_left = 3
gameover = False
restart = False
angle = 0
speed = 0
pause = False
printGameOver = True

house_area = [{'x': 10, 'y': 20, 'health': 100, 'condition': 'normal','color': [[0.9, 0.6, 0.1], [0.7, 0.5, 0.1]],'originalColor': [[0.9, 0.6, 0.1], [0.7, 0.5, 0.1]]},
                {'x': 10, 'y': 220, 'health': 100, 'condition': 'normal','color': [[1.0, 0.0, 0.5], [0.5, 0.0, 0.3]],'originalColor': [[1.0, 0.0, 0.5], [0.5, 0.0, 0.3]]},
                {'x': 10, 'y': 420, 'health': 100, 'condition': 'normal','color': [[0.9, 0.0, 1.0], [0.5, 0.0, 0.6]],'originalColor': [[0.9, 0.0, 1.0], [0.5, 0.0, 0.6]]},
                {'x': 640, 'y': 20, 'health': 100, 'condition': 'normal','color': [[0.1, 0.3, 1.0], [0.0, 0.2, 0.7]],'originalColor': [[0.1, 0.3, 1.0], [0.0, 0.2, 0.7]]},
                {'x': 640, 'y': 220, 'health': 100, 'condition': 'normal','color': [[0.2, 0.4, 0.2], [0.2, 0.2, 0.2]],'originalColor': [[0.2, 0.4, 0.2], [0.2, 0.2, 0.2]]},
                {'x': 640, 'y': 420, 'health': 100, 'condition': 'normal','color': [[1, 0.5, 0.6], [0.3, 0.3, 0.4]],'originalColor': [[1, 0.5, 0.6], [0.3, 0.3, 0.4]]}]

HouseHealth = [[25, 180, 45 + house_area[0]['health'], 180], [25, 380, 45 + house_area[1]['health'], 380],
                [25, 580, 45 + house_area[2]['health'], 580], [655, 180, 675 + house_area[3]['health'], 180],
                [655, 380, 675 + house_area[4]['health'], 380], [655, 580, 675 + house_area[5]['health'], 580]]

# ------------------------ MIDPOINT LINE DRAWING ALGORITHM START ------------------------

def draw_Point(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def Find_Zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6

def Convert_To_Zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def Convert_To_Original_Zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def Mid_Point_Line_Algorithm(x1, y1, x2, y2):
    zone = Find_Zone(x1, y1, x2, y2)
    
    x1, y1 = Convert_To_Zone_0(x1, y1, zone)
    x2, y2 = Convert_To_Zone_0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1
    y = y1
    while (x <= x2):
        x_original, y_original = Convert_To_Original_Zone(x, y, zone)
        draw_Point(x_original, y_original)
        x += 1
        if d > 0:
            d += dNE
            y = y + 1
        else:
            d += dE


# ------------------------ MIDPOINT LINE DRAWING ALGORITHM END ------------------------

# ------------------------ MIDPOINT CIRCLE DRAWING ALGORITHM START ------------------------


def draw_Points(x, y, dx, dy):
    draw_Point(x + dx, y + dy)
    draw_Point(-x + dx, y + dy)
    draw_Point(-x + dx, -y + dy)
    draw_Point(x + dx, -y + dy)
    draw_Point(y + dx, x + dy)
    draw_Point(-y + dx, x + dy)
    draw_Point(-y + dx, -x + dy)
    draw_Point(y + dx, -x + dy)

def Mid_Point_Circle_Algorithm(x, y, r):
    x0 = 0
    y0 = r
    d = 1 - r
    draw_Points(x0, y0, x, y)
    while (x0 < y0):
        if (d < 0):
            d += (2 * x0 + 3)
            x0 += 1
        else:
            d += ((2 * x0) - (2 * y0) + 5)
            x0 += 1
            y0 -= 1
        draw_Points(x0, y0, x, y)


# ------------------------ MIDPOINT CIRCLE DRAWING ALGORITHM END ------------------------

# ------------------------ DRAW HOUSES ------------------------

def Draw_Houses(x1, y1, color1, color2):

    glPointSize(25)
    glColor3f(0.2, 0.7, 0.8)
    Mid_Point_Line_Algorithm(x1 + 37, y1 + 90, x1 + 37, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 70, y1 + 90, x1 + 70, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 80, y1 + 90, x1 + 80, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 112, y1 + 90, x1 + 112, y1 + 20)
    
    glPointSize(2)
    glColor3f(0.2, 0.2, 0.2)
    Mid_Point_Line_Algorithm(x1 + 38, y1 + 90, x1 + 38, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 75, y1 + 90, x1 + 75, y1 + 50)
    Mid_Point_Line_Algorithm(x1 + 112, y1 + 90, x1 + 112, y1 + 20)
    
    Mid_Point_Line_Algorithm(x1 + 20, y1 + 73, x1 + 130, y1 + 73)
    Mid_Point_Line_Algorithm(x1 + 60, y1 + 38, x1 + 20, y1 + 38)
    Mid_Point_Line_Algorithm(x1 + 100, y1 + 38, x1 + 130, y1 + 38)
    
    Mid_Point_Line_Algorithm(x1 + 75, y1 + 50, x1 + 75, y1 + 10)
    Mid_Point_Circle_Algorithm(x1 + 70, y1 + 32, 1)
    Mid_Point_Circle_Algorithm(x1 + 80, y1 + 32, 1)
    
    glPointSize(12)
    if (gameover == False):
        glColor3f(*color1)
    else:
        glColor3f(1, 1, 1)

    Mid_Point_Line_Algorithm(x1 + 25, y1 + 90, x1 + 125, y1 + 90)
    Mid_Point_Line_Algorithm(x1 + 25, y1 + 55, x1 + 125, y1 + 55)
    Mid_Point_Line_Algorithm(x1 + 25, y1 + 20, x1 + 55, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 95, y1 + 20, x1 + 125, y1 + 20)
    
    Mid_Point_Line_Algorithm(x1 + 20, y1 + 90, x1 + 20, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 55, y1 + 90, x1 + 55, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 95, y1 + 90, x1 + 95, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 130, y1 + 90, x1 + 130, y1 + 20)
    
    glPointSize(8)
    glColor3f(0.2, 0.2, 0.2)
    Mid_Point_Line_Algorithm(x1 + 10, y1 + 10, x1 + 140, y1 + 10)
    Mid_Point_Line_Algorithm(x1 + 12, y1 + 100, x1 + 138, y1 + 100)
    
    glPointSize(4)
    glColor3f(0.5, 0.5, 0.5)
    Mid_Point_Line_Algorithm(x1 + 72, y1 + 128, x1 + 77, y1 + 128)
    Mid_Point_Line_Algorithm(x1 + 66, y1 + 124, x1 + 85, y1 + 124)
    Mid_Point_Line_Algorithm(x1 + 58, y1 + 120, x1 + 93, y1 + 120)
    Mid_Point_Line_Algorithm(x1 + 50, y1 + 116, x1 + 101, y1 + 116)
    Mid_Point_Line_Algorithm(x1 + 40, y1 + 112, x1 + 111, y1 + 112)
    Mid_Point_Line_Algorithm(x1 + 32, y1 + 108, x1 + 119, y1 + 108)
    Mid_Point_Line_Algorithm(x1 + 29, y1 + 105, x1 + 122, y1 + 105)
    
    glPointSize(2)
    glColor3f(1, 1, 0)
    Mid_Point_Line_Algorithm(x1 + 72, y1 + 120, x1 + 72, y1 + 110)
    Mid_Point_Circle_Algorithm(x1 + 75, y1 + 118, 3)
    Mid_Point_Circle_Algorithm(x1 + 75, y1 + 112, 3)
    
    glPointSize(3)
    glColor3f(0.2, 0.2, 0.2)
    Mid_Point_Line_Algorithm(x1 + 28, y1 + 104, x1 + 122, y1 + 104)
    Mid_Point_Line_Algorithm(x1 + 20, y1 + 102, x1 + 75, y1 + 130)
    Mid_Point_Line_Algorithm(x1 + 75, y1 + 130, x1 + 130, y1 + 102)
    
    glPointSize(2)
    glColor3f(0.5, 0.5, 0.5)
    
    Mid_Point_Line_Algorithm(x1 + 12, y1 + 15, x1 + 138, y1 + 15)
    Mid_Point_Line_Algorithm(x1 + 12, y1 + 95, x1 + 138, y1 + 95)
    Mid_Point_Line_Algorithm(x1 + 8, y1 + 102, x1 + 142, y1 + 102)
    Mid_Point_Line_Algorithm(x1 + 5, y1 + 8, x1 + 145, y1 + 8)
    
    glPointSize(8)
    glColor3f(0.5, 0.5, 0.5)
    Mid_Point_Line_Algorithm(x1 + 20, y1 + 90, x1 + 20, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 55, y1 + 90, x1 + 55, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 95, y1 + 90, x1 + 95, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 130, y1 + 90, x1 + 130, y1 + 20)
    
    glPointSize(2)
    glColor3f(0.2, 0.2, 0.2)
    Mid_Point_Line_Algorithm(x1 + 18, y1 + 90, x1 + 18, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 22, y1 + 90, x1 + 22, y1 + 20)
    
    Mid_Point_Line_Algorithm(x1 + 53, y1 + 90, x1 + 53, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 57, y1 + 90, x1 + 57, y1 + 20)
    
    Mid_Point_Line_Algorithm(x1 + 93, y1 + 90, x1 + 93, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 97, y1 + 90, x1 + 97, y1 + 20)
    
    Mid_Point_Line_Algorithm(x1 + 128, y1 + 90, x1 + 128, y1 + 20)
    Mid_Point_Line_Algorithm(x1 + 132, y1 + 90, x1 + 132, y1 + 20)


def Draw_House():
    global HouseHealth, pause, gameover, house_area

    for house in house_area:
        if (gameover == False and pause == False):
            if (house['condition'] == 'looting'):
                house['color'] = [[1, 0, 0], [0.4, 0, 0]]
                house['health'] -= 1

            if (house['condition'] == 'looting' and house['health'] <= 5):
                house['condition'] = 'looted'
                house['health'] = 0

            if (house['condition'] == 'looted'):
                house['color'] = [[0.7, 0.7, 0.7], [0.7, 0.7, 0.7]]
        Draw_Houses(house['x'], house['y'], house['color'][0], house['color'][1])


def Draw_HouseHealth():
    global HouseHealth
    for i in range(len(HouseHealth)):
        glPointSize(10)
        glColor3f(0.8, 0, 0)
        Mid_Point_Line_Algorithm(HouseHealth[i][0], HouseHealth[i][1], HouseHealth[i][2], HouseHealth[i][3])
        

# ------------------------ DRAW Roads ------------------------

def Draw_RoadLines():
    glPointSize(12)
    glColor3f(0.7, 0.5, 0)
    Mid_Point_Line_Algorithm(400, 560, 400, 510)
    Mid_Point_Line_Algorithm(400, 460, 400, 410)
    Mid_Point_Line_Algorithm(400, 360, 400, 310)
    Mid_Point_Line_Algorithm(400, 260, 400, 210)
    Mid_Point_Line_Algorithm(400, 160, 400, 110)
    Mid_Point_Line_Algorithm(400, 60, 400, 30)


# ------------------------ DRAW TANK ------------------------

def Draw_Tank():
    global angle, tank
    tx = -40
    ty = -75
    glTranslatef(tank['x'], tank['y'], 0.0)
    glRotatef(angle, 0, 0, 1)
    # draw wheel of the tank
    glPointSize(5)
    glColor3f(0, 0, 0)
    # left wheels
    Mid_Point_Circle_Algorithm(tx, ty + 15, 5)
    Mid_Point_Circle_Algorithm(tx, ty + 30, 5)
    Mid_Point_Circle_Algorithm(tx, ty + 45, 5)
    Mid_Point_Circle_Algorithm(tx, ty + 60, 5)
    Mid_Point_Circle_Algorithm(tx, ty + 75, 5)
    Mid_Point_Circle_Algorithm(tx, ty + 90, 5)
    # right wheels
    Mid_Point_Circle_Algorithm(tx + 79, ty + 15, 5)
    Mid_Point_Circle_Algorithm(tx + 79, ty + 30, 5)
    Mid_Point_Circle_Algorithm(tx + 79, ty + 45, 5)
    Mid_Point_Circle_Algorithm(tx + 79, ty + 60, 5)
    Mid_Point_Circle_Algorithm(tx + 79, ty + 75, 5)
    Mid_Point_Circle_Algorithm(tx + 79, ty + 90, 5)
    
    Mid_Point_Circle_Algorithm(tx + 40, ty + 155, 2)
    
    glPointSize(9)
    if (gameover == False):
        glColor3f(0.2, 0, 0)
    else:
        glColor3f(0, 0, 0)
        
    Mid_Point_Circle_Algorithm(tx + 15, ty - 3, 3)
    Mid_Point_Circle_Algorithm(tx + 65, ty - 3, 3)
    
    glPointSize(4)
    glColor3f(0, 0, 0)
    Mid_Point_Line_Algorithm(tx, ty, tx, ty + 110)
    Mid_Point_Line_Algorithm(tx + 20, ty + 115, tx + 60, ty + 115)
    Mid_Point_Line_Algorithm(tx, ty + 110, tx + 20, ty + 110)
    Mid_Point_Line_Algorithm(tx + 60, ty + 110, tx + 80, ty + 110)
    Mid_Point_Line_Algorithm(tx + 80, ty + 110, tx + 80, ty)
    Mid_Point_Line_Algorithm(tx, ty - 5, tx + 80, ty - 5)

    if (gameover == False):
        glColor3f(179 / 255, 0, 0)
    else:
        glColor3f(0.2, 0.2, 0.2)

    glPointSize(20)
    if (gameover == False):
        glColor3f(0.1, 0.1, 0)
    else:
        glColor3f(0.2, 0.2, 0.2)
    Mid_Point_Line_Algorithm(tx + 10, ty + 5, tx + 10, ty + 100)
    Mid_Point_Line_Algorithm(tx + 20, ty + 5, tx + 20, ty + 105)
    Mid_Point_Line_Algorithm(tx + 30, ty + 5, tx + 30, ty + 105)
    Mid_Point_Line_Algorithm(tx + 40, ty + 5, tx + 40, ty + 105)
    Mid_Point_Line_Algorithm(tx + 50, ty + 5, tx + 50, ty + 105)
    Mid_Point_Line_Algorithm(tx + 60, ty + 5, tx + 60, ty + 105)
    Mid_Point_Line_Algorithm(tx + 70, ty + 5, tx + 70, ty + 100)

    glPointSize(5)
    if (gameover == False):
        glColor3f(1, 1, 1)
    else:
        glColor3f(0, 0, 0)
        
    Mid_Point_Circle_Algorithm(tx + 14, ty + 118, 1)
    Mid_Point_Circle_Algorithm(tx + 66, ty + 118, 1)
    
    glPointSize(9)
    if (gameover == False):
        glColor3f(0.2, 0.2, 0)
    else:
        glColor3f(0, 0, 0)
    Mid_Point_Line_Algorithm(tx + 14, ty + 115, tx + 14, ty + 115)
    Mid_Point_Line_Algorithm(tx + 66, ty + 115, tx + 66, ty + 115)
    
    glPointSize(5)
    if (gameover == False):
        glColor3f(200 / 255, 51 / 255, 51 / 255)
    else:
        glColor3f(0.2, 0.2, 0.2)
        
    glPointSize(2)
    glColor3f(0, 0, 0)
    Mid_Point_Line_Algorithm(tx + 10, ty - 5, tx + 10, ty + 100)
    Mid_Point_Line_Algorithm(tx + 10, ty + 100, tx + 70, ty + 100)
    Mid_Point_Line_Algorithm(tx + 70, ty - 5, tx + 70, ty + 100)
        
    glPointSize(20)
    if (gameover == False):
        glColor3f(0.1, 0.2, 0)
    else:
        glColor3f(0.2, 0.2, 0.2)
    Mid_Point_Line_Algorithm(tx + 20, ty + 5, tx + 20, ty + 90)
    Mid_Point_Line_Algorithm(tx + 30, ty + 5, tx + 30, ty + 90)
    Mid_Point_Line_Algorithm(tx + 40, ty + 5, tx + 40, ty + 90)
    Mid_Point_Line_Algorithm(tx + 50, ty + 5, tx + 50, ty + 90)
    Mid_Point_Line_Algorithm(tx + 60, ty + 5, tx + 60, ty + 90)

    glPointSize(8)
    if (gameover == False):
        glColor3f(0, 0.1, 0)
    else:
        glColor3f(0, 0, 0)
    Mid_Point_Line_Algorithm(tx + 40, ty + 70, tx + 40, ty + 150)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 80, 4)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 150, 4)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 70, 8)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 40, 9)
    
    glPointSize(30)
    if (gameover == False):
        glColor3f(0, 0.1, 0)
    else:
        glColor3f(0, 0, 0)
    Mid_Point_Line_Algorithm(tx + 40, ty + 50, tx + 40, ty + 60)
    
    glPointSize(2)
    if (gameover == False):
        glColor3f(0.1, 0, 0)
    else:
        glColor3f(0, 0, 0)
    
    Mid_Point_Circle_Algorithm(tx + 20, ty + 90, 1)
    Mid_Point_Circle_Algorithm(tx + 60, ty + 90, 1)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 55, 8)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 55, 4)
    Mid_Point_Circle_Algorithm(tx + 40, ty + 35, 2)
    Mid_Point_Circle_Algorithm(tx + 20, ty + 10, 5)
    Mid_Point_Circle_Algorithm(tx + 20, ty + 10, 1)
    Mid_Point_Circle_Algorithm(tx + 30, ty, 1)
    Mid_Point_Circle_Algorithm(tx + 60, ty + 10, 5)
    Mid_Point_Circle_Algorithm(tx + 60, ty + 10, 1)
    Mid_Point_Circle_Algorithm(tx + 50, ty, 1)


# ------------------------ DRAW Bullets ------------------------

def Draw_Bullet():
    glPointSize(4)
    glColor3f(0, 0, 0)
    Mid_Point_Circle_Algorithm(0, 155, 4)
    Mid_Point_Circle_Algorithm(20, 140, 4)
    Mid_Point_Circle_Algorithm(-20, 140, 4)
    Mid_Point_Circle_Algorithm(0, 110, 4)
    Mid_Point_Circle_Algorithm(0, 155, 1)
    Mid_Point_Circle_Algorithm(20, 140, 1)
    Mid_Point_Circle_Algorithm(-20, 140, 1)
    Mid_Point_Circle_Algorithm(0, 110, 1)


# ------------------------ DRAW Buttons ------------------------

def Draw_Cross():
    glPointSize(4)
    glColor3f(1, 0.1, 0)
    Mid_Point_Line_Algorithm(740, 640, 780, 680)
    Mid_Point_Line_Algorithm(780, 640, 740, 680)

def Draw_Restart():
    glPointSize(4)
    glColor3f(0, 0.8, 0.5)
    Mid_Point_Line_Algorithm(20, 660, 70, 660)
    Mid_Point_Line_Algorithm(20, 660, 40, 680)
    Mid_Point_Line_Algorithm(20, 660, 40, 640)

def Draw_Pause():
    glColor3f(1, 1, 0)
    glPointSize(6)
    Mid_Point_Line_Algorithm(385, 640, 385, 680)
    Mid_Point_Line_Algorithm(415, 640, 415, 680)

def Draw_Play():
    glPointSize(4)
    glColor3f(0.2, 1, 0)
    Mid_Point_Line_Algorithm(385, 640, 385, 680)
    Mid_Point_Line_Algorithm(385, 640, 420, 660)
    Mid_Point_Line_Algorithm(385, 680, 420, 660)


# ------------------------ DISPLAY SCORE AND FAST TRAVEL ------------------------

def Render_Text(string, x, y, font):
    glRasterPos2f(x, y)
    for character in string:
        glutBitmapCharacter(font, ord(character)) # type: ignore
        
def Show_Score():
    global Score
    glColor3f(0.2, 1, 0)
    Score_text = f"Your Score: {Score}"
    Render_Text(Score_text, 150, 650,  GLUT_BITMAP_TIMES_ROMAN_24) # type: ignore
    
def Show_Fast_Travel_Left():
    global fast_travel_left
    glColor3f(0.2, 1, 0)
    life_text = f"Fast Travel Left: {fast_travel_left}"
    Render_Text(life_text, 500, 650,  GLUT_BITMAP_TIMES_ROMAN_24) # type: ignore
    
    
# ------------------------ KEYBOARD AND MOUSE COMMANDS ------------------------

def SpecialKeyListener(key, x, y):
    global angle, tank, Bullet, pause, gameover

    if (gameover == False and pause == False):
        if key == GLUT_KEY_RIGHT:
            angle = -90
            if (tank['x'] + 30 <= 570):
                tank['x'] += 30
            tank['direction'] = 'right'
            Bullet = False
        if key == GLUT_KEY_LEFT:
            angle = 90
            if (tank['x'] - 30 >= 230):
                tank['x'] -= 30
            tank['direction'] = 'left'
            Bullet = False
        if key == GLUT_KEY_UP:
            angle = 0
            if (tank['y'] + 30 <= 500):
                tank['y'] += 30
            tank['direction'] = 'up'
            Bullet = False
        if key == GLUT_KEY_DOWN:
            angle = 180
            if (tank['y'] - 30 >= 80):
                tank['y'] -= 30
            tank['direction'] = 'down'
            Bullet = False
            
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global Bullet, gameover, pause
    if (gameover == False and pause == False):
        if key == b' ':
            Bullet = not Bullet
            
    glutPostRedisplay()

def MouseListener(button, state, x, y):
    global tank, fast_travel_left, Score, restart, pause, gameover
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            if (x >= 230 and x <= 570 and y >= 220 and fast_travel_left > 0 and gameover == False and pause == False):
                tank['x'] = x
                tank['y'] = 720 - y
                fast_travel_left -= 1
            print("Fast Travel Left:", fast_travel_left)
            
            if (x >= 720 and y <= 70):
                print("Goodbye! Score:", Score)
                glutLeaveMainLoop()
            if (x <= 70 and y <= 70):
                restart = True
            if (x > 370 and y < 70 and x < 430):
                pause =  not pause

    glutPostRedisplay()


# ------------------------ ANIMATIONS ------------------------

def Animation():
    glutPostRedisplay()
    global fireTimer, HouseHealth, Bullet, Score, fast_travel_left, gameover, tank, house_area, restart, printGameOver, speed, pause
    speed += 0.005

    if (gameover == False and pause == False):

        if (fireTimer <= 0):
            random_integer = random.randint(0, 5)
            house_area[random_integer]['condition'] = 'looting'
            fireTimer = 100
            
        fireTimer -= (3 + speed)

        HouseHealth = [[25, 180, 45 + house_area[0]['health'], 180], [25, 380, 45 + house_area[1]['health'], 380],
                        [25, 580, 45 + house_area[2]['health'], 580], [655, 180, 675 + house_area[3]['health'], 180],
                        [655, 380, 675 + house_area[4]['health'], 380], [655, 580, 675 + house_area[5]['health'], 580]]

        if ((tank['y'] <= 130) and (tank['y'] >= 50) and (tank['direction'] == 'left')):
            if ((tank['x'] <= 310) and Bullet == True and house_area[0]['condition'] != 'looted'):
                if (house_area[0]['health'] <= 95):
                    house_area[0]['health'] += 3 
                    if (house_area[0]['health'] >= 95):
                        house_area[0]['condition'] = 'normal'
                        Score += 1
                        print('Score:', Score)
                        house_area[0]['health'] = 100
                        house_area[0]['color'] = house_area[0]['originalColor']

        if ((tank['y'] <= 330) and (tank['y'] >= 250) and (tank['direction'] == 'left')):
            if ((tank['x'] <= 310) and Bullet == True and house_area[1]['condition'] != 'looted'):
                if (house_area[1]['health'] <= 95):
                    house_area[1]['health'] += 3
                    if (house_area[1]['health'] >= 95):
                        house_area[1]['condition'] = 'normal'
                        Score += 1
                        print('Score:', Score)
                        house_area[1]['health'] = 100
                        house_area[1]['color'] = house_area[1]['originalColor']

        if ((tank['y'] <= 530) and (tank['y'] >= 450) and (tank['direction'] == 'left')):
            if ((tank['x'] <= 310) and Bullet == True and house_area[2]['condition'] != 'looted'):
                if (house_area[2]['health'] <= 95):
                    house_area[2]['health'] += 3
                    if (house_area[2]['health'] >= 95):
                        house_area[2]['condition'] = 'normal'
                        Score += 1
                        print('Score:', Score)
                        house_area[2]['health'] = 100
                        house_area[2]['color'] = house_area[2]['originalColor']

        if ((tank['y'] <= 130) and (tank['y'] >= 50) and (tank['direction'] == 'right')):
            if ((tank['x'] >= 490) and Bullet == True and house_area[3]['condition'] != 'looted'):
                if (house_area[3]['health'] <= 95):
                    house_area[3]['health'] += 3
                    if (house_area[3]['health'] >= 95):
                        house_area[3]['condition'] = 'normal'
                        Score += 1
                        print('Score:', Score)
                        house_area[3]['health'] = 100
                        house_area[3]['color'] = house_area[3]['originalColor']

        if ((tank['y'] <= 330) and (tank['y'] >= 250) and (tank['direction'] == 'right')):
            if ((tank['x'] >= 490) and Bullet == True and house_area[4]['condition'] != 'looted'):
                if (house_area[4]['health'] <= 95):
                    house_area[4]['health'] += 3
                    if (house_area[4]['health'] >= 95):
                        house_area[4]['condition'] = 'normal'
                        Score += 1
                        print('Score:', Score)
                        house_area[4]['health'] = 100
                        house_area[4]['color'] = house_area[4]['originalColor']
                        
        if ((tank['y'] <= 530) and (tank['y'] >= 450) and (tank['direction'] == 'right')):
            if ((tank['x'] >= 490) and Bullet == True and house_area[5]['condition'] != 'looted'):
                if (house_area[5]['health'] <= 95):
                    house_area[5]['health'] += 3
                    if (house_area[5]['health'] >= 95):
                        house_area[5]['condition'] = 'normal'
                        Score += 1
                        print('Score:', Score)
                        house_area[5]['health'] = 100
                        house_area[5]['color'] = house_area[5]['originalColor']
                        

    if (restart == True):
        restart = False
        tank = {'x': 400, 'y': 400, 'direction': 'up'}
        gameover = False
        
        house_area = [{'x': 10, 'y': 20, 'health': 100, 'condition': 'normal','color': [[0.9, 0.6, 0.1], [0.7, 0.5, 0.1]],'originalColor': [[0.9, 0.6, 0.1], [0.7, 0.5, 0.1]]},
                    {'x': 10, 'y': 220, 'health': 100, 'condition': 'normal','color': [[1.0, 0.0, 0.5], [0.5, 0.0, 0.3]],'originalColor': [[1.0, 0.0, 0.5], [0.5, 0.0, 0.3]]},
                    {'x': 10, 'y': 420, 'health': 100, 'condition': 'normal','color': [[0.9, 0.0, 1.0], [0.5, 0.0, 0.6]],'originalColor': [[0.9, 0.0, 1.0], [0.5, 0.0, 0.6]]},
                    {'x': 640, 'y': 20, 'health': 100, 'condition': 'normal','color': [[0.1, 0.3, 1.0], [0.0, 0.2, 0.7]],'originalColor': [[0.1, 0.3, 1.0], [0.0, 0.2, 0.7]]},
                    {'x': 640, 'y': 220, 'health': 100, 'condition': 'normal','color': [[0.2, 0.4, 0.2], [0.2, 0.2, 0.2]],'originalColor': [[0.2, 0.4, 0.2], [0.2, 0.2, 0.2]]},
                    {'x': 640, 'y': 420, 'health': 100, 'condition': 'normal','color': [[1, 0.5, 0.6], [0.3, 0.3, 0.4]],'originalColor': [[1, 0.5, 0.6], [0.3, 0.3, 0.4]]}]

        HouseHealth = [[25, 180, 45 + house_area[0]['health'], 180], [25, 380, 45 + house_area[1]['health'], 380],
                        [25, 580, 45 + house_area[2]['health'], 580], [655, 180, 675 + house_area[3]['health'], 180],
                        [655, 380, 675 + house_area[4]['health'], 380], [655, 580, 675 + house_area[5]['health'], 580]]
        
        Bullet = False
        Score = 0
        fast_travel_left = 3
        printGameOver = True
        pause = False
        speed = 0
        

def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
def Display():
    global Bullet, gameover, Score, printGameOver
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.1, 0.1, 0.1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    Draw_RoadLines()
    glColor3f(1, 0, 0)
    Draw_Cross()
    glColor3f(0.5, 1.0, 1.0)
    Draw_Restart()
    
    if ( gameover == False and pause == False):
        Draw_Pause()
    elif (gameover == False and pause == True):
        Draw_Play()
    
    if (gameover == False):
        Show_Score()
        Show_Fast_Travel_Left()
    
    if (gameover == True):
        glColor3f(1, 0, 0)
        Render_Text("Game Over..!", 335, 650, GLUT_BITMAP_TIMES_ROMAN_24) # type: ignore
        glColor3f(0.2, 1, 0)
        Score_text = f"Your Score: {Score}"
        Render_Text(Score_text, 335, 610, GLUT_BITMAP_TIMES_ROMAN_24) # type: ignore
        
    Draw_HouseHealth()
    Draw_House()
    Draw_Tank()
    
    num_looted = 0
    for house in house_area:
        if (house['condition'] == 'looted'):
            num_looted += 1
        if (num_looted >= 3):
            gameover = True
            if (printGameOver == True):
                print("Game Over!")
                print('Score:', Score)
            printGameOver = False
        
    if (Bullet == True):
        glColor3f(0.0, 0.9, 0.9)
        Draw_Bullet()
    
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 700)
glutInitWindowPosition(400, 25)
wind = glutCreateWindow(b"Money Heist Game!")
glutIdleFunc(Animation)
glutDisplayFunc(Display)
glutSpecialFunc(SpecialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(MouseListener)
glutMainLoop()