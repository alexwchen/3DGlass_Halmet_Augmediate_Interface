#!/usr/bin/env python
import cv2
import cv
import time
from operation import *

thickness = 2
font_height = 0.7
font_weight = 0.7
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, font_height, font_weight, 0, thickness, 8) #Creates a font

def draw_menu_button(ir_ipl, rgb_ipl, status_dictionary, start_time):
    # create a copy of the original:
    ir_overlay = cv.CloneImage(ir_ipl)
    rgb_overlay = cv.CloneImage(rgb_ipl)

    # cvCircle Method (img, center, radius, color, thickness, lineType, shift);
    for b in status_dictionary:
        if b=='b4':
            continue
        button = status_dictionary[b]
        button_status = button[0] # True, False (selected, not selected)
        button_pos = button[1]
        button_radius = button[2]
        button_color = button[3]
        button_text = button[4]
        text_pos = button[5]
        text_color = button[6]
        butoon_action_list = button[7] # 0->null, 1->hover, 2->click
        butoon_hover_state = button[8] # Ture, False

        if butoon_hover_state == True: # check for Hover first
            cv.Circle(ir_ipl, button_pos, button_radius+10, button_color, -1)
            cv.Circle(rgb_ipl, button_pos, button_radius+10, button_color, -1)

            if button_status:
                cv.PutText(ir_ipl, button_text, text_pos, font, text_color)
                cv.PutText(rgb_ipl, button_text, text_pos, font, text_color)
                cv.PutText(ir_ipl, 'on', (text_pos[0]+15, text_pos[1]+15), font, text_color)
                cv.PutText(rgb_ipl, 'on', (text_pos[0]+15, text_pos[1]+15), font, text_color)
            else:
                cv.PutText(ir_ipl, button_text, text_pos, font, text_color)
                cv.PutText(rgb_ipl, button_text, text_pos, font, text_color)

        elif button_status == True: # if not hovered, might be selected
            cv.Circle(ir_ipl, button_pos, button_radius, button_color, -1)
            cv.Circle(rgb_ipl, button_pos, button_radius, button_color, -1)
            cv.PutText(ir_ipl, button_text, text_pos, font, text_color)
            cv.PutText(rgb_ipl, button_text, text_pos, font, text_color)
            cv.PutText(ir_ipl, 'on', (text_pos[0]+15, text_pos[1]+15), font, text_color)
            cv.PutText(rgb_ipl, 'on', (text_pos[0]+15, text_pos[1]+15), font, text_color)

        elif button_status == False: # if not selected, nothing happen
            cv.Circle(ir_ipl, button_pos, button_radius, button_color, -1)
            cv.Circle(rgb_ipl, button_pos, button_radius, button_color, -1)
            cv.PutText(ir_ipl, button_text, text_pos, font, text_color)
            cv.PutText(rgb_ipl, button_text, text_pos, font, text_color)

    # Draw Drag Box
    if status_dictionary['b2'][0]:
        button = status_dictionary['b4']
        button_status = button[0] # True, False (selected, not selected)
        button_pos = button[1]
        button_radius = button[2]
        button_color = button[3]
        button_text = button[4]
        text_pos = button[5]
        text_color = button[6]
        butoon_action_list = button[7] # 0->null, 1->hover, 2->click
        butoon_hover_state = button[8] # Ture, False
        if butoon_hover_state == True: # check for Hover first
            cv.Circle(ir_ipl, button_pos, button_radius+10, button_color, -1)
            cv.Circle(rgb_ipl, button_pos, button_radius+10, button_color, -1)
            cv.PutText(ir_ipl, button_text, text_pos, font, text_color)
            cv.PutText(rgb_ipl, button_text, text_pos, font, text_color)
        else:
            cv.Circle(ir_ipl, button_pos, button_radius, button_color, -1)
            cv.Circle(rgb_ipl, button_pos, button_radius, button_color, -1)
            cv.PutText(ir_ipl, button_text, text_pos, font, text_color)
            cv.PutText(rgb_ipl, button_text, text_pos, font, text_color)




    # blend with the original:
    opacity = 0.4
    cv.AddWeighted(ir_overlay, opacity, ir_ipl, 1 - opacity, 0, ir_ipl)
    cv.AddWeighted(rgb_overlay, opacity, rgb_ipl, 1 - opacity, 0, rgb_ipl)

    # Recording on, print time
    if status_dictionary['b1'][0]:
        t = time.time()
        text = str(t - start_time) + ' sec'
        cv.PutText(rgb_ipl, text, (10,20), font, (255,0,0))

    return ir_ipl, rgb_ipl


def update_button_status(contour_list, history_prediction, Labels, status_dictionary, history_gesture_pos, debug, start_time):

    if debug:
        print contour_list
        print history_prediction

    # Check for cursor gestures 4,5,6,7,11,12
    cursor_gesture_list = [4,5,6,7,11,12]
    if history_prediction[-1] in cursor_gesture_list:
        # --- Do smoothing later if needed ---

        # Calculate if the top left corner is in the button area
        # --- Now this only works for right handed people ---

        # Check which button we are "Hovering"
        for b in status_dictionary:

            # this is drag box
            if b=='b4':
                continue

            button = status_dictionary[b]
            button_status = button[0] # True, False (selected, not selected)
            button_pos = button[1]
            button_radius = button[2]
            button_color = button[3]
            button_text = button[4]
            text_pos = button[5]
            text_color = button[6]
            butoon_action_list = button[7] # 0->null, 1->hover, 2->click
            butoon_hover_state = button[8] # Ture, False
            gesture_pos = contour_list[0] # (x,y,w,h)

            # Hover
            # check if guesture pos lies in button bounding box
            condition_x = (gesture_pos[0]>=(button_pos[0]-button_radius) and gesture_pos[0]<=(button_pos[0]+button_radius))
            condition_y = (gesture_pos[1]>=(button_pos[1]-button_radius) and gesture_pos[1]<=(button_pos[1]+button_radius))
            if condition_x and condition_y and (1 not in butoon_action_list):
                butoon_hover_state = True
                button[8] = butoon_hover_state
                button[0] = 1 - button[0]

                if debug:
                    #print 'Hovering'
                    #print status_dictionary
                    pass

                # update action list
                if len(butoon_action_list) >= 7:
                    del butoon_action_list[0]
                    butoon_action_list.append(1)
                else:
                    butoon_action_list.append(1)

            # no action is happening, append null to action
            else:
                # not hovered
                butoon_hover_state = False
                button[8] = butoon_hover_state

                # no action for clicking
                if len(butoon_action_list) >= 7:
                    del butoon_action_list[0]
                    butoon_action_list.append(0)
                else:
                    butoon_action_list.append(0)
            """
            # Click
            # check if the gesture size decreases
            if len(history_prediction) > 5 and len(history_gesture_pos) > 5 and (2 not in butoon_action_list):
                condition_1 = (history_prediction[-2] in cursor_gesture_list)
                condition_2 = (history_prediction[-3] in cursor_gesture_list)

                # Selected
                if button_status == False and condition_1 and condition_2 and butoon_hover_state:
                    his_pos_1 = history_gesture_pos[-2]
                    his_pos_2 = history_gesture_pos[-3]
                    size_1 = his_pos_1[2]*his_pos_1[3]
                    size_2 = his_pos_2[2]*his_pos_2[3]
                    cur_size = gesture_pos[2]*gesture_pos[3]

                    if debug:
                        print 'Check Size???', size_1, size_2, cur_size
                        pass

                    if cur_size < size_1 and cur_size < size_2 and size_1 < size_2 and (size_1 - cur_size > 5000):
                        button_status = True
                        button[0] = button_status

                        if debug:
                            print 'select!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                            #print status_dictionary

                        # update action list
                        if len(butoon_action_list) >= 7:
                            del butoon_action_list[0]
                            butoon_action_list.append(2)
                        else:
                            butoon_action_list.append(2)


                # UnSelected
                elif button_status == True and condition_1 and condition_2 and butoon_hover_state:
                    his_pos_1 = history_gesture_pos[-2]
                    his_pos_2 = history_gesture_pos[-3]
                    size_1 = his_pos_1[2]*his_pos_1[3]
                    size_2 = his_pos_2[2]*his_pos_2[3]
                    cur_size = gesture_pos[2]*gesture_pos[3]
                    if cur_size < size_1 and cur_size < size_2 and size_1 < size_2 and (size_1 - cur_size > 5000):
                        button_status = False
                        button[0] = button_status

                        if debug:
                            print 'select!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                            #print status_dictionary

                        # update action list
                        if len(butoon_action_list) >= 7:
                            del butoon_action_list[0]
                            butoon_action_list.append(2)
                        else:
                            butoon_action_list.append(2)
            else:
                # no action for clicking
                if len(butoon_action_list) >= 7:
                    del butoon_action_list[0]
                    butoon_action_list.append(0)
                else:
                    butoon_action_list.append(0)
            """

            #print 'butoon_action_list', butoon_action_list
            button[7] = butoon_action_list

    if status_dictionary['b1'][0]:
        start_time = time.time()


    # Drag Box check
    # Check for cursor gestures 4,5,6,7,11,12
    cursor_gesture_list = [4,5,6,7,11,12]
    if (history_prediction[-1] in cursor_gesture_list) and status_dictionary['b2']:
            button = status_dictionary['b4']
            button_status = button[0] # True, False (selected, not selected)
            button_pos = button[1]
            button_radius = button[2]
            button_color = button[3]
            button_text = button[4]
            text_pos = button[5]
            text_color = button[6]
            butoon_action_list = button[7] # 0->null, 1->hover, 2->click
            butoon_hover_state = button[8] # Ture, False
            gesture_pos = contour_list[0] # (x,y,w,h)

            # Hover
            # check if guesture pos lies in button bounding box
            condition_x = (gesture_pos[0]-30>=(button_pos[0]-button_radius) and gesture_pos[0]-30<=(button_pos[0]+button_radius))
            condition_y = (gesture_pos[1]-30>=(button_pos[1]-button_radius) and gesture_pos[1]-30<=(button_pos[1]+button_radius))
            if condition_x and condition_y and (1 not in butoon_action_list):
                butoon_hover_state = True
                button[8] = butoon_hover_state
            else:
                butoon_hover_state = False
                button[8] = butoon_hover_state

    if len(history_prediction) > 5:
        cursor_gesture_list = [2,3,9,10]
        #condition1 = (history_prediction[-2] or history_prediction[-3] in cursor_gesture_list)
        if (history_prediction[-1] in cursor_gesture_list) and status_dictionary['b2']:
                button = status_dictionary['b4']
                button_status = button[0] # True, False (selected, not selected)
                button_pos = button[1]
                button_radius = button[2]
                button_color = button[3]
                button_text = button[4]
                text_pos = button[5]
                text_color = button[6]
                butoon_action_list = button[7] # 0->null, 1->hover, 2->click
                butoon_hover_state = button[8] # Ture, False
                gesture_pos = contour_list[0] # (x,y,w,h)

                # Hover
                # check if guesture pos lies in button bounding box
                condition_x = (gesture_pos[0]>=(button_pos[0]-button_radius) and gesture_pos[0]<=(button_pos[0]+button_radius))
                condition_y = (gesture_pos[1]>=(button_pos[1]-button_radius) and gesture_pos[1]<=(button_pos[1]+button_radius))
                if condition_x and condition_y:
                    button[1] = (gesture_pos[0], gesture_pos[1])
                    button[5] = (gesture_pos[0]-30, gesture_pos[1]-30)

    return status_dictionary, start_time

