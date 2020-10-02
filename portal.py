import math
import random
from datetime import datetime, timedelta
import os
import time
import turtle

# For less jerky player movement you can uncomment the grayed out code, comment out the four current player movement code lines, and set SPEED to 4

SPEED = 20
PORTAL_SPEED = 30
GLIDE_DURATION_IN_SECONDS = 4

ice_speed = 15

ice_state = False

control_menu_showing = True

set_time_a = datetime.now()
set_time_b = datetime.now()

looper = "left"

acquired_portal_gun = False
orange_portal_state = "ready"
blue_portal_state = "ready"

portal_gun_acquired_sound = ["a"]

turret_sound_bucket = []
turret_lost_bucket = []

up_token_bucket = []
down_token_bucket = []
left_token_bucket = []
right_token_bucket = []

turret_sounds = ["afplay turret_there_you_are.wav&", "afplay turret_I_see_you.wav&", "afplay turret_gotcha.wav&"]
portal_gun_gifs = ["portal_gun_up.gif", "portal_gun_down.gif", "portal_gun_left.gif", "portal_gun_right.gif", "control_menu.gif"]

for gif in portal_gun_gifs:
    turtle.register_shape(gif)

# Sets the start glide times just over the GLIDE_DURATION_IN_SECONDS to prevent uncommanded gliding
global STARTED_GLIDING_UP_AT
STARTED_GLIDING_UP_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)

global STARTED_GLIDING_RIGHT_AT
STARTED_GLIDING_RIGHT_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)

global STARTED_GLIDING_LEFT_AT
STARTED_GLIDING_LEFT_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)

global STARTED_GLIDING_DOWN_AT
STARTED_GLIDING_DOWN_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)

# Game screen
screen = turtle.Screen()
screen.bgpic("portal.gif")
screen.bgcolor("gray")
screen.title("Enemy AI - Worlds")
screen.tracer(0)

# Game border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("black")
border_pen.penup()
border_pen.setposition(-500, -500)
border_pen.pendown()
border_pen.pensize(8)
for side in range(4):
    border_pen.fd(1000)
    border_pen.lt(90)
border_pen.hideturtle()

# Control menu
control_menu = turtle.Turtle()
control_menu.speed(0)
control_menu.penup()
control_menu.setposition(0,0)
control_menu.shape("control_menu.gif")
control_menu.hideturtle()

# Player
player = turtle.Turtle()
player.speed(0)
player.penup()
player.color("darkorange")
player.shape("circle")
player.setheading(90)
player.setposition(0,-375)

# Enemy AI
enemy_ai = turtle.Turtle()
enemy_ai.speed(0)
enemy_ai.penup()
enemy_ai.color("white")
enemy_ai.shape("square")
enemy_ai.setheading(270)
enemy_ai.setposition(0,375)

# Poratl gun
portal_gun = turtle.Turtle()
portal_gun.speed(0)
portal_gun.shape("portal_gun_right.gif")
portal_gun.penup()
portal_gun.setposition(-375,0)

# Orange portal 
orange_portal = turtle.Turtle()
orange_portal.color("orange")
orange_portal.shape("circle")
orange_portal.penup()
orange_portal.speed(0)
orange_portal.shapesize(0.5,0.5)
orange_portal.hideturtle()
orange_portal.setposition(1000,1000)

# Blue portal
blue_portal = turtle.Turtle()
blue_portal.color("lightblue")
blue_portal.shape("circle")
blue_portal.penup()
blue_portal.speed(0)
blue_portal.shapesize(0.5,0.5)
blue_portal.hideturtle()
blue_portal.setposition(1000,1000)

# Player movements / checking proximity of player and portal / portal travel
def move_up():
    player.setheading(90)
    player.sety(player.ycor() + SPEED)
    # # An option for smoother player movement, but messes with the portal functionality 
    # length = len(up_token_bucket)
    # for _ in range(10-length):
    #     up_token_bucket.append("a")
    if player.ycor() >= orange_portal.ycor() and player.xcor() >= (orange_portal.xcor() - 45) and player.xcor() <= (orange_portal.xcor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.ycor() >= blue_portal.ycor() and player.xcor() >= (blue_portal.xcor() - 45) and player.xcor() <= (blue_portal.xcor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()


def move_down():
    player.setheading(270)
    player.sety(player.ycor() - SPEED)
    # # An option for smoother player movement, but messes with the portal functionality 
    # length = len(down_token_bucket)
    # for _ in range(10-length):
    #     down_token_bucket.append("a")
    if player.ycor() <= orange_portal.ycor() and player.xcor() >= (orange_portal.xcor() - 45) and player.xcor() <= (orange_portal.xcor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.ycor() <= blue_portal.ycor() and player.xcor() >= (blue_portal.xcor() - 45) and player.xcor() <= (blue_portal.xcor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()


def move_left():
    player.setheading(180)
    player.setx(player.xcor() - SPEED)
    # # An option for smoother player movement, but messes with the portal functionality 
    # length = len(left_token_bucket)
    # for _ in range(10-length):
    #     left_token_bucket.append("a")
    if player.xcor() <= orange_portal.xcor() and player.ycor() >= (orange_portal.ycor() - 45) and player.ycor() <= (orange_portal.ycor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.xcor() <= blue_portal.xcor() and player.ycor() >= (blue_portal.ycor() - 45) and player.ycor() <= (blue_portal.ycor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()


def move_right():
    player.setheading(0)
    player.setx(player.xcor() + SPEED)
    # # An option for smoother player movement, but messes with the portal functionality 
    # length = len(right_token_bucket)
    # for _ in range(10-length):
    #     right_token_bucket.append("a")
    if player.xcor() >= orange_portal.xcor() and player.ycor() >= (orange_portal.ycor() - 45) and player.ycor() <= (orange_portal.ycor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.xcor() >= blue_portal.xcor() and player.ycor() >= (blue_portal.ycor() - 45) and player.ycor() <= (blue_portal.ycor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()

# An option for smoother player movement, but messes with the portal functionality
def up():
    player.sety(player.ycor() + SPEED)
def down():
    player.sety(player.ycor() - SPEED)
def left():
    player.setx(player.xcor() - SPEED)
def right():
    player.setx(player.xcor() + SPEED)


# Ice floor movements
def up_ice():
    player.sety(player.ycor() + ice_speed)
    if player.ycor() >= orange_portal.ycor() and player.xcor() >= (orange_portal.xcor() - 45) and player.xcor() <= (orange_portal.xcor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.ycor() >= blue_portal.ycor() and player.xcor() >= (blue_portal.xcor() - 45) and player.xcor() <= (blue_portal.xcor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()
def down_ice():
    player.sety(player.ycor() + ice_speed)
    if player.ycor() <= orange_portal.ycor() and player.xcor() >= (orange_portal.xcor() - 45) and player.xcor() <= (orange_portal.xcor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.ycor() <= blue_portal.ycor() and player.xcor() >= (blue_portal.xcor() - 45) and player.xcor() <= (blue_portal.xcor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()
def left_ice():
    player.setx(player.xcor() + ice_speed)
    if player.xcor() <= orange_portal.xcor() and player.ycor() >= (orange_portal.ycor() - 45) and player.ycor() <= (orange_portal.ycor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.xcor() <= blue_portal.xcor() and player.ycor() >= (blue_portal.ycor() - 45) and player.ycor() <= (blue_portal.ycor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()
def right_ice():
    player.setx(player.xcor() + ice_speed)
    if player.xcor() >= orange_portal.xcor() and player.ycor() >= (orange_portal.ycor() - 45) and player.ycor() <= (orange_portal.ycor() + 45) and is_touching_portal(player, orange_portal):
        blue_portal_check()
    if player.xcor() >= blue_portal.xcor() and player.ycor() >= (blue_portal.ycor() - 45) and player.ycor() <= (blue_portal.ycor() + 45) and is_touching_portal(player, blue_portal):
        orange_portal_check()


# Check how the player exits the blue portal
def blue_portal_check():
    os.system("afplay exit_warp.wav&")
    if blue_portal.ycor() == -500:
        player.setheading(90)
        player.setposition(blue_portal.xcor(), blue_portal.ycor() + 46)
    if blue_portal.ycor() == 500:
        player.setheading(270)
        player.setposition(blue_portal.xcor(), blue_portal.ycor() - 46)
    if blue_portal.xcor() == -500:
        player.setheading(0)
        player.setposition(blue_portal.xcor() + 46, blue_portal.ycor())
    if blue_portal.xcor() == 500:
        player.setheading(180)
        player.setposition(blue_portal.xcor() - 46, blue_portal.ycor())


# Check how the player exits the orange portal
def orange_portal_check():
    os.system("afplay exit_warp.wav&")
    if orange_portal.ycor() == -500:
        player.setheading(90)
        player.setposition(orange_portal.xcor(), orange_portal.ycor() + 46)
    if orange_portal.ycor() == 500:
        player.setheading(270)
        player.setposition(orange_portal.xcor(), orange_portal.ycor() - 46)
    if orange_portal.xcor() == -500:
        player.setheading(0)
        player.setposition(orange_portal.xcor() + 46, orange_portal.ycor())
    if orange_portal.xcor() == 500:
        player.setheading(180)
        player.setposition(orange_portal.xcor() - 46, orange_portal.ycor())


# Resets the starting glide times to the current time 
def ice_move_up():
    player.setheading(90)
    global STARTED_GLIDING_UP_AT
    STARTED_GLIDING_UP_AT = datetime.now()


def ice_move_down():
    player.setheading(270)
    global STARTED_GLIDING_DOWN_AT
    STARTED_GLIDING_DOWN_AT = datetime.now()


def ice_move_left():
    player.setheading(180)
    global STARTED_GLIDING_LEFT_AT
    STARTED_GLIDING_LEFT_AT = datetime.now()


def ice_move_right():
    player.setheading(0)
    global STARTED_GLIDING_RIGHT_AT
    STARTED_GLIDING_RIGHT_AT = datetime.now()


# Enemy AI is idle by default, but will follow the player when approached 
def enemy_ai_active():
    global set_time
    global set_time_a
    global set_time_b
    if is_in_proximity(enemy_ai, player):
        follow_player(enemy_ai)
        set_time_a = datetime.now()
        set_time_b = datetime.now()
        for _ in range(1 - len(turret_lost_bucket)):
            turret_lost_bucket.append("a")
        if turret_sound_bucket:
            os.system(random.choice(turret_sounds))
            turret_sound_bucket.pop()
    else:
        set_time = datetime.now()
        enemy_ai_idle_state()
        for _ in range(1 - len(turret_sound_bucket)):
            turret_sound_bucket.append("a")
        if turret_lost_bucket:
            os.system("afplay turret_target_lost.wav&")
            turret_lost_bucket.pop()


# Follows the player
def follow_player(x):
    if player.xcor() > x.xcor():
        x.setx(x.xcor() + 1.5)
    if player.xcor() < x.xcor():
        x.setx(x.xcor() - 1.5)
    if player.ycor() < x.ycor():
        x.sety(x.ycor() - 1.5)
    if player.ycor() > x.ycor():
        x.sety(x.ycor() + 1.5)

    
# Attaches the portal gun to the player once the player and portal gun are in proximity
def equipped_portal_gun():
    global acquired_portal_gun
    if is_touching(portal_gun, player):
        acquired_portal_gun = True
        if portal_gun_acquired_sound:
            os.system("afplay handheld_portal_device.wav&")
            portal_gun_acquired_sound.pop()

    if acquired_portal_gun:
        # UP
        if player.heading() == 90:
            portal_gun.setposition(player.xcor()-15, player.ycor()+5)
            portal_gun.shape("portal_gun_up.gif")
        # DOWN
        if player.heading() == 270:
            portal_gun.setposition(player.xcor()+16, player.ycor()-3)
            portal_gun.shape("portal_gun_down.gif")
        # LEFT
        if player.heading() == 180:
            portal_gun.setposition(player.xcor()-4, player.ycor()-15)
            portal_gun.shape("portal_gun_left.gif")
        # RIGHT
        if player.heading() == 0:
            portal_gun.setposition(player.xcor()+5, player.ycor()+15)
            portal_gun.shape("portal_gun_right.gif")


# Has the enemy go in circles according to two timers constantly switching back and forth. This could aslo be achieved with a for loop with fd() and lt()
def enemy_ai_idle_state():
    global set_time_a
    global set_time_b
    global looper

    running_time_a = datetime.now()
    elapsed_time_a = running_time_a - set_time_a
    sec_a = elapsed_time_a.total_seconds()

    running_time_b = datetime.now()
    elapsed_time_b = running_time_b - set_time_b
    sec_b = elapsed_time_b.total_seconds()

    if sec_a < 1 and looper == "left":
        enemy_ai.setx(enemy_ai.xcor()-1)
        set_time_b = datetime.now()
        if sec_a > .8:
            looper = "down"
    if sec_b < 1 and looper == "down":
        enemy_ai.sety(enemy_ai.ycor()-1)
        set_time_a = datetime.now()
        if sec_b > .8:
            looper = "right"
    if sec_a <= 1 and looper == "right":
        enemy_ai.setx(enemy_ai.xcor()+1)
        set_time_b = datetime.now()
        if sec_a > .8:
            looper = "up"
    if sec_b <= 1 and looper == "up":
        enemy_ai.sety(enemy_ai.ycor()+1)
        set_time_a = datetime.now()
        if sec_b > .8:
            looper = "left"


def fire_orange_portal_up():
    global orange_portal_state
    if orange_portal_state == "ready":
        player.setheading(90)
        portal_gun.setposition(player.xcor()-15, player.ycor()+5)
        orange_portal.shapesize(0.5, 0.5)
        orange_portal.setheading(90)
        os.system("afplay portal_fire.wav&")
        orange_portal_state = "fire_up"
        # Move the portal just above the portal gun
        x = portal_gun.xcor()
        y = portal_gun.ycor() + 10
        orange_portal.setposition(x, y)
        orange_portal.showturtle()


def fire_orange_portal_down():
    global orange_portal_state
    if orange_portal_state == "ready":
        player.setheading(270)
        portal_gun.setposition(player.xcor()+16, player.ycor()-3)
        orange_portal.shapesize(0.5, 0.5)
        orange_portal.setheading(270)
        os.system("afplay portal_fire.wav&")
        orange_portal_state = "fire_down"
        # Move the portal just below the portal gun
        x = portal_gun.xcor()
        y = portal_gun.ycor() - 10
        orange_portal.setposition(x, y)
        orange_portal.showturtle()


def fire_orange_portal_left():
    global orange_portal_state
    if orange_portal_state == "ready":
        player.setheading(180)
        portal_gun.setposition(player.xcor()-4, player.ycor()-15)
        orange_portal.shapesize(0.5, 0.5)
        orange_portal.setheading(180)
        os.system("afplay portal_fire.wav&")
        orange_portal_state = "fire_left"
        # Move the portal to just left of the portal gun
        x = portal_gun.xcor() - 10
        y = portal_gun.ycor()
        orange_portal.setposition(x, y)
        orange_portal.showturtle()


def fire_orange_portal_right():
    global orange_portal_state
    if orange_portal_state == "ready":
        player.setheading(0)
        portal_gun.setposition(player.xcor()+5, player.ycor()+15)
        orange_portal.shapesize(0.5, 0.5)
        orange_portal.setheading(0)
        os.system("afplay portal_fire.wav&")
        orange_portal_state = "fire_right"
        # Move the weapon to just right of the portal gun
        x = portal_gun.xcor() + 10
        y = portal_gun.ycor()
        orange_portal.setposition(x, y)
        orange_portal.showturtle()


def fire_blue_portal_up():
    global blue_portal_state
    if blue_portal_state == "ready":
        player.setheading(90)
        portal_gun.setposition(player.xcor()-15, player.ycor()+5)
        blue_portal.shapesize(0.5, 0.5)
        blue_portal.setheading(90)
        os.system("afplay portal_fire.wav&")
        blue_portal_state = "fire_up"
        # Move the portal just above the portal gun
        x = portal_gun.xcor()
        y = portal_gun.ycor() + 10
        blue_portal.setposition(x, y)
        blue_portal.showturtle()


def fire_blue_portal_down():
    global blue_portal_state
    if blue_portal_state == "ready":
        player.setheading(270)
        portal_gun.setposition(player.xcor()+16, player.ycor()-3)
        blue_portal.shapesize(0.5, 0.5)
        blue_portal.setheading(270)
        os.system("afplay portal_fire.wav&")
        blue_portal_state = "fire_down"
        # Move the portal just below the portal gun
        x = portal_gun.xcor()
        y = portal_gun.ycor() - 10
        blue_portal.setposition(x, y)
        blue_portal.showturtle()


def fire_blue_portal_left():
    global blue_portal_state
    if blue_portal_state == "ready":
        player.setheading(180)
        portal_gun.setposition(player.xcor()-4, player.ycor()-15)
        blue_portal.shapesize(0.5, 0.5)
        blue_portal.setheading(180)
        os.system("afplay portal_fire.wav&")
        blue_portal_state = "fire_left"
        # Move the portal to just left of the portal gun
        x = portal_gun.xcor() - 10
        y = portal_gun.ycor()
        blue_portal.setposition(x, y)
        blue_portal.showturtle()


def fire_blue_portal_right():
    global blue_portal_state
    if blue_portal_state == "ready":
        player.setheading(0)
        portal_gun.setposition(player.xcor()+5, player.ycor()+15)
        blue_portal.shapesize(0.5, 0.5)
        blue_portal.setheading(0)
        os.system("afplay portal_fire.wav&")
        blue_portal_state = "fire_right"
        # Move the portal to just right of the portal gun
        x = portal_gun.xcor() + 10
        y = portal_gun.ycor()
        blue_portal.setposition(x, y)
        blue_portal.showturtle()


def control_menu_switch():
    global control_menu_showing
    if control_menu_showing == False:
        control_menu_showing = True
    elif control_menu_showing == True:
        control_menu_showing = False


def menu_check():
    if control_menu_showing == True:
        control_menu.showturtle()
    if control_menu_showing == False:
        control_menu.hideturtle()


def ice_switch():
    global ice_state
    if ice_state == False:
        ice_state = True
    elif ice_state == True:
        ice_state = False


def ice_floor_check():
    if ice_state == True:
        screen.listen()
        screen.onkeypress(ice_move_up, "Up")
        screen.onkeypress(ice_move_down, "Down")
        screen.onkeypress(ice_move_left, "Left")
        screen.onkeypress(ice_move_right, "Right")
        screen.bgpic("portal_ice.gif")
    if ice_state == False:
        screen.listen()
        screen.onkeypress(move_up, "Up")
        screen.onkeypress(move_down, "Down")
        screen.onkeypress(move_left, "Left")
        screen.onkeypress(move_right, "Right")
        screen.bgpic("portal.gif")
        
        global STARTED_GLIDING_UP_AT
        STARTED_GLIDING_UP_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)
        global STARTED_GLIDING_RIGHT_AT
        STARTED_GLIDING_RIGHT_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)
        global STARTED_GLIDING_LEFT_AT
        STARTED_GLIDING_LEFT_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)
        global STARTED_GLIDING_DOWN_AT
        STARTED_GLIDING_DOWN_AT = datetime.now() - timedelta(seconds=GLIDE_DURATION_IN_SECONDS + 1)


# Touching / proximity calculations
def is_touching(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


def is_touching_portal(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 45:
        return True
    else:
        return False


def is_in_proximity(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 200:
        return True
    else:
        return False

# Keyboard bindings
screen.listen()
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(ice_switch, "i")
screen.onkeypress(control_menu_switch, "m")

while True:
    screen.update()
    enemy_ai_active()
    equipped_portal_gun()
    ice_floor_check()
    menu_check()

    # # An option for smoother player movement, but messes with the portal functionality 
    if up_token_bucket:
        up()
        up_token_bucket.pop()
    if down_token_bucket:
        down()
        down_token_bucket.pop()
    if left_token_bucket:
        left()
        left_token_bucket.pop()
    if right_token_bucket:
        right()
        right_token_bucket.pop()

    # If the player acquires the portal gun, they now have access to it with the corresponding keys
    if acquired_portal_gun == True:
        screen.listen()
        screen.onkeypress(fire_orange_portal_up, "w")
        screen.onkeypress(fire_orange_portal_down, "s")
        screen.onkeypress(fire_orange_portal_left, "a")
        screen.onkeypress(fire_orange_portal_right, "d")
        screen.onkeypress(fire_blue_portal_up, "t")
        screen.onkeypress(fire_blue_portal_down, "g")
        screen.onkeypress(fire_blue_portal_left, "f")
        screen.onkeypress(fire_blue_portal_right, "h")

    # Move the orange portal
    if orange_portal_state == "fire_up":
        y = orange_portal.ycor()
        y += PORTAL_SPEED
        orange_portal.sety(y)

    if orange_portal_state == "fire_down":
        y = orange_portal.ycor()
        y += PORTAL_SPEED * -1
        orange_portal.sety(y)

    if orange_portal_state == "fire_left":
        x = orange_portal.xcor()
        x += PORTAL_SPEED * -1
        orange_portal.setx(x)

    if orange_portal_state == "fire_right":
        x = orange_portal.xcor()
        x += PORTAL_SPEED
        orange_portal.setx(x)

    if orange_portal.ycor() > 490:
        orange_portal.setposition(orange_portal.xcor(), 500)
        orange_portal.shape("square")
        orange_portal.shapesize(5, .4)
        orange_portal_state = "ready"
    if orange_portal.ycor() < -490:
        orange_portal.setposition(orange_portal.xcor(), -500)
        orange_portal.shape("square")
        orange_portal.shapesize(5, .4)
        orange_portal_state = "ready"
    if orange_portal.xcor() > 490:
        orange_portal.setposition(500, orange_portal.ycor())
        orange_portal.shape("square")
        orange_portal.shapesize(5, .4)
        orange_portal_state = "ready"
    if orange_portal.xcor() < -490:
        orange_portal.setposition(-500, orange_portal.ycor())
        orange_portal.shape("square")
        orange_portal.shapesize(5, .4)
        orange_portal_state = "ready"

    # Move the blue portal
    if blue_portal_state == "fire_up":
        y = blue_portal.ycor()
        y += PORTAL_SPEED
        blue_portal.sety(y)

    if blue_portal_state == "fire_down":
        y = blue_portal.ycor()
        y += PORTAL_SPEED * -1
        blue_portal.sety(y)

    if blue_portal_state == "fire_left":
        x = blue_portal.xcor()
        x += PORTAL_SPEED * -1
        blue_portal.setx(x)

    if blue_portal_state == "fire_right":
        x = blue_portal.xcor()
        x += PORTAL_SPEED
        blue_portal.setx(x)

    # Check to see if the weapon has reached the game border
    if blue_portal.ycor() > 490:
        blue_portal.setposition(blue_portal.xcor(), 500)
        blue_portal.shape("square")
        blue_portal.shapesize(5, .4)
        blue_portal_state = "ready"
    if blue_portal.ycor() < -490:
        blue_portal.setposition(blue_portal.xcor(), -500)
        blue_portal.shape("square")
        blue_portal.shapesize(5, .4)
        blue_portal_state = "ready"
    if blue_portal.xcor() > 490:
        blue_portal.setposition(500, blue_portal.ycor())
        blue_portal.shape("square")
        blue_portal.shapesize(5, .4)
        blue_portal_state = "ready"
    if blue_portal.xcor() < -490:
        blue_portal.setposition(-500, blue_portal.ycor())
        blue_portal.shape("square")
        blue_portal.shapesize(5, .4)
        blue_portal_state = "ready"

    # Ice floor glide calculations
    if datetime.now() - STARTED_GLIDING_UP_AT <= timedelta(seconds=GLIDE_DURATION_IN_SECONDS):
        elapsed_time = datetime.now() - STARTED_GLIDING_UP_AT
        glide_numerator = 1
        glide_denominator = max([glide_numerator, elapsed_time.total_seconds()])
        speed = glide_numerator / glide_denominator
        ice_speed = speed
        up_ice()

    if datetime.now() - STARTED_GLIDING_DOWN_AT <= timedelta(seconds=GLIDE_DURATION_IN_SECONDS):
        elapsed_time = datetime.now() - STARTED_GLIDING_DOWN_AT
        glide_numerator = 1
        glide_denominator = max([glide_numerator, elapsed_time.total_seconds()])
        speed = glide_numerator / glide_denominator
        ice_speed = speed * -1
        down_ice()

    if datetime.now() - STARTED_GLIDING_LEFT_AT <= timedelta(seconds=GLIDE_DURATION_IN_SECONDS):
        elapsed_time = datetime.now() - STARTED_GLIDING_LEFT_AT
        glide_numerator = 1
        glide_denominator = max([glide_numerator, elapsed_time.total_seconds()])
        speed = glide_numerator / glide_denominator
        ice_speed = speed * -1
        left_ice()

    if datetime.now() - STARTED_GLIDING_RIGHT_AT <= timedelta(seconds=GLIDE_DURATION_IN_SECONDS):
        elapsed_time = datetime.now() - STARTED_GLIDING_RIGHT_AT
        glide_numerator = 1
        glide_denominator = max([glide_numerator, elapsed_time.total_seconds()])
        speed = glide_numerator / glide_denominator
        ice_speed = speed
        right_ice()
