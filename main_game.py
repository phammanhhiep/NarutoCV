# import time
import numpy as np
import imutils
import pygame
import cv2
import global_variables as gb
import game_ops
from game_ops import Jutsu
import visual_ops
from visual_ops import CharacterIcon, Button, VisualCue, Jutsu_Icon 
import predict_ops
import camera_ops
from keras import models


# ------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------------------------------------------------------

# Camera Variables
# bg = None
calibrate = 30
WIDTH = 165
HEIGHT = 235
top, right, bottom, left = 195, 255, 430, 420  # far away
aWeight = 0.5

# Model Prediction Variables
saved_model = "./VGG16_LR_0.0003_EPOCHS1_1571499473.7668839"
model = models.load_model(saved_model)
num_frames = 0
count = 0
mean_cutoff = 70
accumulated_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
top_signs = []
sequence = []

# PyGame Variables
player_turn = True
clicked_away = False
attack = False
active_health = 0
active_damage = 0

pygame.init()


# Jutsu Sign Variables
signs = ['bird', 'boar', 'dog', 'dragon', 'hare', 'horse', 'monkey', 'ox', 'ram', 'rat', 'serpent', 'tiger']
bird = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
boar = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
dog = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
dragon = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
hare = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
horse = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
monkey = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
ox = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
ram = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
rat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
serpent = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
tiger = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]


# ----------------------------------------------------------------------------------------
# GAME OBJECTS INSTANTIATION
# ----------------------------------------------------------------------------------------
player1_character1_icon = CharacterIcon('kakashi', 1, 1, win=gb.win)
player1_character2_icon = CharacterIcon('obito', 1, 2, win=gb.win)
player1_character3_icon = CharacterIcon('guy', 1, 3, win=gb.win)
player2_character1_icon = CharacterIcon('crow', 2, 1, win=gb.win)
player2_character2_icon = CharacterIcon('akamaru', 2, 2, win=gb.win)
player2_character3_icon = CharacterIcon('naruto', 2, 3, win=gb.win)

player1_character1_jutsu1_icon = Jutsu_Icon(icon_name='Kakashi Sharingan', player_num=1, icon_num=1, parent_icon=player1_character1_icon, win=gb.win)
player1_character1_jutsu2_icon = Jutsu_Icon('Ninja Hounds', 1, 2, player1_character1_icon, win=gb.win)
player1_character1_jutsu3_icon = Jutsu_Icon('Lightning Blade', 1, 3, player1_character1_icon, win=gb.win)
player1_character1_jutsu4_icon = Jutsu_Icon('Hiding', 1, 4, player1_character1_icon, win=gb.win)

player1_character2_jutsu1_icon = Jutsu_Icon(icon_name='Tobi Chains', player_num=1, icon_num=1, parent_icon=player1_character2_icon, win=gb.win)
player1_character2_jutsu2_icon = Jutsu_Icon('Tobi Kamui', 1, 2, player1_character2_icon, win=gb.win)
player1_character2_jutsu3_icon = Jutsu_Icon('Summoning Nine Tails', 1, 3, player1_character2_icon, win=gb.win)
player1_character2_jutsu4_icon = Jutsu_Icon('Rin', 1, 4, player1_character2_icon, win=gb.win)

player1_character3_jutsu1_icon = Jutsu_Icon(icon_name='Guy Leaf Whirl Wind', player_num=1, icon_num=1, parent_icon=player1_character3_icon, win=gb.win)
player1_character3_jutsu2_icon = Jutsu_Icon('Counter Punch', 1, 2, player1_character3_icon, win=gb.win)
player1_character3_jutsu3_icon = Jutsu_Icon('6th Gate of Joy', 1, 3, player1_character3_icon, win=gb.win)
player1_character3_jutsu4_icon = Jutsu_Icon('Guy Dodge', 1, 4, player1_character3_icon, win=gb.win)
 
player2_character1_jutsu1_icon = Jutsu_Icon(icon_name='Rasengan', player_num=2, icon_num=1, parent_icon=player2_character3_icon, win=gb.win)
player2_character1_jutsu2_icon = Jutsu_Icon('Shadow Clone Jutsu', 2, 2, player2_character3_icon, win=gb.win)
player2_character1_jutsu3_icon = Jutsu_Icon('Chakra Boost', 2, 3, player2_character3_icon, win=gb.win)
player2_character1_jutsu4_icon = Jutsu_Icon('Shadow Save', 2, 4, player2_character3_icon, win=gb.win)

player2_character2_jutsu1_icon = Jutsu_Icon(icon_name='Crow Stab', player_num=2, icon_num=1, parent_icon=player2_character1_icon, win=gb.win)
player2_character2_jutsu2_icon = Jutsu_Icon('Crow Poison Bomb', 2, 2, player2_character1_icon, win=gb.win)
player2_character2_jutsu3_icon = Jutsu_Icon('Crow Black Ant', 2, 3, player2_character1_icon, win=gb.win)
player2_character2_jutsu4_icon = Jutsu_Icon('Crow Substitution', 2, 4, player2_character1_icon, win=gb.win)

player2_character3_jutsu1_icon = Jutsu_Icon(icon_name='Fang over Fang', player_num=2, icon_num=1, parent_icon=player2_character2_icon, win=gb.win)
player2_character3_jutsu2_icon = Jutsu_Icon('Dynamic Marking', 2, 2, player2_character2_icon, win=gb.win)
player2_character3_jutsu3_icon = Jutsu_Icon('Double Headed Wolf', 2, 3, player2_character2_icon, win=gb.win)
player2_character3_jutsu4_icon = Jutsu_Icon('Puppy mode', 2, 4, player2_character2_icon, win=gb.win)

background = pygame.image.load("env_icons/background2.jpg")
background = pygame.transform.scale(background, (gb.display_width, gb.display_height))

pygame.mixer.init()
pygame.mixer.music.load("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
pygame.mixer.music.play(-1)


# ----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":

    game = True
    jutsu = False

    while True:

        while game:

            # PyGame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # KEY PRESSES
                if event.type == pygame.KEYDOWN:
                    print('keydown')
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_t:
                        player_turn = not player_turn
                        CharacterIcon.class_turn = player_turn
                    if event.key == pygame.K_RETURN:
                        print("Enter")
                        attack = not attack

            # Background
            gb.win.fill(gb.orange)
            gb.win.blit(background, (0,0))

            player1_character1_icon.display_image()
            player1_character2_icon.display_image()
            player1_character3_icon.display_image()
            player2_character1_icon.display_image()
            player2_character2_icon.display_image()
            player2_character3_icon.display_image()

            player1_character1_jutsu1_icon.display_image()
            player1_character1_jutsu2_icon.display_image()
            player1_character1_jutsu3_icon.display_image()
            player1_character1_jutsu4_icon.display_image()
            player1_character2_jutsu1_icon.display_image()
            player1_character2_jutsu2_icon.display_image()
            player1_character2_jutsu3_icon.display_image()
            player1_character2_jutsu4_icon.display_image()
            player1_character3_jutsu1_icon.display_image()
            player1_character3_jutsu2_icon.display_image()
            player1_character3_jutsu3_icon.display_image()
            player1_character3_jutsu4_icon.display_image()

            player2_character1_jutsu1_icon.display_image()
            player2_character1_jutsu2_icon.display_image()
            player2_character1_jutsu3_icon.display_image()
            player2_character1_jutsu4_icon.display_image()
            player2_character2_jutsu1_icon.display_image()
            player2_character2_jutsu2_icon.display_image()
            player2_character2_jutsu3_icon.display_image()
            player2_character2_jutsu4_icon.display_image()
            player2_character3_jutsu1_icon.display_image()
            player2_character3_jutsu2_icon.display_image()
            player2_character3_jutsu3_icon.display_image()

            click = pygame.mouse.get_pressed()

            if attack and Jutsu_Icon.jutsu_que != [] and CharacterIcon.attacked_queue != []:  # attack was previously attack_button.is_clicked
                gb.win.fill((255, 255, 255))
                select = Jutsu_Icon.jutsu_que
                selected_jutsu = Jutsu(icon=select, parent_icon=select.parent_icon, attacking_player=player_turn)
                attacked_character = CharacterIcon.attacked_queue
                active_health = attacked_character.health
                active_damage = selected_jutsu.get_damage()
                # attacked_character.health -= active_damage
                procedure = visual_ops.prepare(selected_jutsu, gb.win)
                gb.win.fill(gb.white)
                camera = camera_ops.setup_camera()
                jutsu = True
                game = False
                attack = False  # attack_button.is_clicked = False
                pygame.mixer_music.stop()
                pygame.mixer_music.load("Sound/Naruto OST 1 - Need To Be Strong.mp3")
                pygame.mixer_music.play(-1)

            # ----------------------------------------------------
            # Final Update
            pygame.display.update()

            # Reset buttons
            # test_button.is_clicked = False
            # attack_button.is_clicked = False
            Button.class_clickable = False

            Jutsu_Icon.class_clickable = False
            CharacterIcon.char_highlighted = False

        # -----------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------
        # COMPUTER VISION & HAND SIGNS SECTION
        # -----------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------
        while jutsu:

            procedure.create_cue()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            (grabbed, frame) = camera.read()

            # -------------------------
            # BUTTON CONTROLS (MOSTLY)
            # -------------------------
            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q"):
                break

            # ------------------------------------
            # COMPUTER VISION OPERATIONS ON FRAME
            # ------------------------------------
            frame = imutils.resize(frame, width=700)  # resize the frame
            frame = cv2.flip(frame, 1)  # flip the frame so that it is not the mirror view
            clone = frame.copy()  # clone the frame
            (height, width) = frame.shape[:2]  # get the height and width of the frame
            roi = frame[top:bottom, right:left]  # get the ROI
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # convert the roi to grayscale
            gray = cv2.GaussianBlur(gray, (7, 7), 0)  # blur it

            if num_frames < calibrate:  # Calibrate the background for 'calibrate' # of frames (30 frames = 1 seconds)
                camera_ops.run_avg(gray, aWeight)
            else:  # After a background is obtained, threshold/segment the hand/foreground
                hand = camera_ops.segment(gray)

                if hand is not None:
                    (thresholded, segmented) = hand
                    cv2.imshow("Threshold", thresholded)  # display the threshold frame
                    thresholded = np.stack((thresholded,) * 3,
                                           axis=-1)  # Give the binary frame 3 channels for the model

                    # -------------------------
                    # MODEL PREDICTION SECTION
                    # -------------------------

                    # OBTAINING AVERAGE PREDICTIONS, SEQUENCES, AND PERMUTATIONS
                    prediction = model.predict([np.reshape(thresholded, (1, HEIGHT, WIDTH, 3))])
                    count += 1
                    accumulated_predictions += prediction

                    if count % mean_cutoff == 0:
                        average_prediction = accumulated_predictions / mean_cutoff
                        accumulated_predictions = np.zeros_like(prediction)
                        ordered, top_signs, percents = predict_ops.top_three(signs, average_prediction)
                        sequence = predict_ops.create_sequence(sequence, top_signs)

                    perm = predict_ops.permutations(sequence)

                    # -----------------------------
                    # PYGAME VISUAL CUES FOR USER
                    # -----------------------------
                    begin = VisualCue("GO!", w=gb.display_width*0.166666, h=gb.display_height*0.125,
                                      text_color=gb.green, typ='header', seq=sequence, win=gb.win)
                    begin.create_cue()

                    move_cue = VisualCue(f'SIGN #{str(len(sequence)+1)}', gb.display_width*0.14583334,
                                         gb.display_height*0.125, gb.green, 'prompt', sequence, gb.win)
                    move_cue.create_cue()

                    # Visual printing of top signs so far
                    if len(sequence) > 0 and top_signs is not None:
                        prediction_cue = VisualCue(str(top_signs[0]), gb.display_width*0.06666667,
                                                   gb.display_height*0.05, gb.green, 'jutsu', sequence, gb.win)
                        prediction_cue.create_cue()
                        for s in top_signs:
                            try:
                                if s == selected_jutsu.get_sequence()[len(sequence)-1]:
                                    print("Thumbs up")
                                    thumbsup = VisualCue(msg=[], w=[], h=[], text_color=(0, 0, 0), typ='image',
                                                         seq=sequence, image_str='character_icons/mightguythumbsup.jpg', win=gb.win)
                                    thumbsup.display_image()
                                    pygame.display.update()
                            except Exception as e:
                                print("exception: ", e)

                    # RESET / FINISHED
                    if selected_jutsu.get_sequence() in perm:
                        attacked_character.health = game_ops.apply_damage(active_health, active_damage)
                        game_ops.success(selected_jutsu)

                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, \
                        game, jutsu = game_ops.reset_game()
                        player_turn = not player_turn
                        pygame.mixer.music.load("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
                        pygame.mixer_music.play()
                        break

                    elif len(sequence) >= len(selected_jutsu.get_sequence()) and selected_jutsu.get_sequence() not in perm:
                        game_ops.failed()

                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, \
                        game, jutsu = game_ops.reset_game()
                        player_turn = not player_turn
                        pygame.mixer.music.load("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
                        pygame.mixer_music.play()
                        break

                    elif keypress == ord("n"):
                        game_ops.failed()

                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, \
                        game, jutsu = game_ops.reset_game()
                        player_turn = not player_turn
                        break

                    pygame.display.update()

            # ----------------------------------
            # AFTER THRESHOLD-PREDICTION PART
            # ----------------------------------
            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)  # draws the box
            num_frames += 1
            # display the original camera frame (with red outline if applicable)
            # cv2.imshow("Video Feed", clone)

        print("Released")
        camera.release()
        cv2.destroyAllWindows()

