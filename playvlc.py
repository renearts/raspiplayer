import pygame
import vlc
import os
import time
import random

# Initialize pygame and VLC
pygame.init()
instance = vlc.Instance()
list_player = instance.media_list_player_new()
player = instance.media_player_new()
list_player.set_media_player(player)

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Detect game controller (use first controller)
num_joysticks = pygame.joystick.get_count()
controllers = [pygame.joystick.Joystick(i) for i in range(num_joysticks)]
for controller in controllers:
    controller.init()

# Get current directory and search for media files
current_dir = os.getcwd()

# Initialize media list for VLC
playlist_path = "Carnaval.m3u"
media_list = instance.media_list_new()

# Search for .mp4 and .mkv files for video
# media_files = []
# for filename in os.listdir(current_dir):
#     if filename.endswith('.mp4') or filename.endswith('.mkv'):
#         media_path = os.path.join(current_dir, filename)
#         if os.path.isfile(media_path):  # Ensure it's a file
#             media_files.append(media_path)

# Check if we found any video files
# if media_files:
#     # Print the video media list with indexes
#     print("Video Files in Directory:")
#     for index, file_path in enumerate(media_files):
#         print(f"{index}: {file_path}")
#
#     # Add media to the media list for VLC
#     for media_path in media_files:
#         media = vlc.Media(media_path)
#         # media_list.add_media(media)
#
#     # player.set_media(media_list[0])  # Start with the first media in the list
# else:
#     print("Error: No valid media files found in the directory.")
#     exit()

# Search for .wav, .mp3, .ogg files for audio
sound_files = []
for filename in os.listdir(current_dir):
    if filename.endswith('.wav') or filename.endswith('.mp3') or filename.endswith('.ogg'):
        sound_path = os.path.join(current_dir, filename)
        if os.path.isfile(sound_path):  # Ensure it's a file
            sound_files.append(sound_path)

# Check if we found any sound files
if sound_files:
    # Print the sound files list with indexes
    print("Sound Files in Directory:")
    for index, file_path in enumerate(sound_files):
        print(f"{index}: {file_path}")
else:
    print("No sound files found in the directory.")

# Keep track of the current media index
current_media_index = 0

# Define button mappings for actions
button_map = {
    'play_pause': 0,    # Button 0 (A) to play/pause
    'stop': 1,          # Button 1 (B) to stop
    'next': 2,          # Button 2 (X) to next
    'previous': 3,      # Button 3 (Y) to previous
    'left_bumper': 4,    # Button 4 to play sound
    'right_bumper': 5,   # Button 4 to play sound
    'select_button': 8, # Button 8 "select"
    'start_video': 9    # Button 5 to select a specific video
}

# D-pad button mapping to sound effects (mapping each D-pad direction to a sound file)
dpad_map = {
    'up': 5,        # D-pad up
    'down': 1,      # D-pad down
    'left': 10,      # D-pad left
    'right': 8      # D-pad right
}

# Dictionary to store the last time a button was pressed
last_press_time = {
    'up': 0,
    'down': 0,
    'left': 0,
    'right': 0
}

# Define the minimum time interval between detections (0.5 seconds for 2 detections per second)
DEBOUNCE_TIME = 0.3

# Function to check if enough time has passed since last press
def can_press(button):
    current_time = time.time()
    if current_time - last_press_time[button] >= DEBOUNCE_TIME:
        last_press_time[button] = current_time
        return True
    return False


# Dictionary to map button presses to sound files
sound_map = {i: sound_files[i] for i in range(len(sound_files))}

def play_media():
    list_player.play()

def pause_media():
    list_player.pause()

def stop_media():
    # global current_media_index
    # current_media_index = instance.get_media()
    # print(f"{current_media_index}")
    list_player.stop()

def next_media():
    list_player.next()
    # global current_media_index
    # current_media_index = (current_media_index + 1) % len(media_files)
    # media = vlc.Media(media_files[current_media_index])
    # player.set_media(media)
    # play_media()        # Check for D-Pad input (axis values)

def previous_media():
    list_player.previous()

def play_sound(file_path):
    sound = pygame.mixer.Sound(file_path)  # Load the sound file
    sound.play()  # Play the sound

def play_random_sound():
    if sound_map:  # Ensure the sound map is not empty
        random_sound = random.choice(list(sound_map.values()))
        play_sound(random_sound)

def read_m3u_file(m3u_path):
    """Reads an M3U file and extracts media file paths."""
    media_files = []
    with open(m3u_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore comments
                media_files.append(line)
    random.shuffle(media_files)
    return media_files

# Main loop for controller input
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                controller_index = event.joy  # Get which controller sent the event

                if controller_index == 0:
                    if button == button_map['play_pause']:  # Play/Pause button
                        print("Play/Pause pressed")
                        if list_player.is_playing():
                            pause_media()
                        else:
                            play_media()
                    elif button == button_map['stop']:  # Stop button
                        print("Stop pressed")
                        stop_media()
                    elif button == button_map['next']:  # Next button
                        print("Next pressed")
                        next_media()
                    elif button == button_map['previous']:  # Previous button
                        print("Previous pressed")
                        previous_media()
                    elif button == button_map['right_bumper']:  # Previous button
                        print("Right bumper pressed")
                        player.set_time(56300)

                    elif button == button_map['left_bumper']:  # Play sound button
                        print("Left bumper pressed")
                        if sound_map:
                            # Play the first sound in the sound_map as an example
                            play_sound(sound_map[0])  # Change to desired button-to-sound mapping
                    elif button == button_map['select_button']:  # Select a specific video
                        print("Select button pressed")
                        # video_index = 7
                        # select_video(video_index)
                        media_list = 0
                        media_list = instance.media_list_new()
                        playlist = read_m3u_file(playlist_path)
                        print("Playlist Contents:")
                        random.shuffle(playlist)
                        for media_file in playlist:
                            media_list.add_media(media_file)
                            print(f"{media_file}")
                        list_player.set_media_list(media_list)
                        list_player.play()

                    elif button == button_map['start_video']:  # Select a specific video
                        print("Start button pressed")
                        list_player.pause()
                        act_media = vlc.Media("/home/mario/20250226 Super Mario Run Jamtoeter compleet.mp4")
                        player.set_media(act_media)
                        player.play()

                    else:
                        print(f"Button {button} pressed on controller {controller_index}")

                elif controller_index == 1:
                    if button == button_map['play_pause']:  # Play/Pause button
                        print("Play/Pause pressed")
                        # if player.is_playing():
                        #     pause_media()
                        # else:
                        # play_media()
                        play_random_sound()
                    elif button == button_map['stop']:  # Stop button
                        print("Stop pressed")
                        # stop_media()
                        play_random_sound()
                    elif button == button_map['next']:  # Next button
                        print("Next pressed")
                        # next_media()
                        play_random_sound()
                    elif button == button_map['previous']:  # Previous button
                        print("Previous pressed")
                        # previous_media()
                        play_random_sound()
                    elif button == button_map['right_bumper']:  # Previous button
                        print("Right bumper pressed")
                        # time_in_ms = 32 * 1000
                        # player.set_time(time_in_ms)
                        play_sound(sound_map[8])
                    elif button == button_map['left_bumper']:  # Play sound button
                        print("Play Sound pressed")
                        play_sound(sound_map[5])
                    elif button == button_map['select_button']:  # Select a specific video
                        print("Select button pressed")
                        # video_index = 2
                        # select_video(video_index)
                        play_random_sound()
                    else:
                        print(f"Button {button} pressed on controller {controller_index}")

        for controller in controllers:
            # Check for D-Pad input (axis values)
            dpad_up = controller.get_axis(1) < -0.5  # D-pad up (negative vertical axis)
            dpad_down = controller.get_axis(1) > 0.5  # D-pad down (positive vertical axis)
            dpad_left = controller.get_axis(0) < -0.5  # D-pad left (negative horizontal axis)
            dpad_right = controller.get_axis(0) > 0.5  # D-pad right (positive horizontal axis)

            # Handle D-pad actions based on input
            if dpad_up and can_press('up'):
                print("D-pad Up pressed")
                if len(sound_map) > dpad_map['up']:
                    play_sound(sound_map[dpad_map['up']])

            elif dpad_down and can_press('down'):
                print("D-pad Down pressed")
                if len(sound_map) > dpad_map['down']:
                    play_sound(sound_map[dpad_map['down']])

            elif dpad_left and can_press('left'):
                print("D-pad Left pressed")
                if len(sound_map) > dpad_map['left']:
                    play_sound(sound_map[dpad_map['left']])

            elif dpad_right and can_press('right'):
                print("D-pad Right pressed")
                if len(sound_map) > dpad_map['right']:
                    play_sound(sound_map[dpad_map['right']])

        time.sleep(0.1)  # Small delay to avoid 100% CPU usage

except KeyboardInterrupt:
    pygame.quit()
    print("Exiting...")
