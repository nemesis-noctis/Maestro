import json
import logging
import os
import subprocess
import threading
import time

import cv2 as cv
import mediapipe as mp

if not os.path.exists("./logs"):
    os.mkdir("./logs")
    
logging.basicConfig(level=logging.INFO, filename='./logs/maestro.log',format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%d/%m/%Y %H:%M:%S')

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode
ClassifierOptions = mp.tasks.components.processors.ClassifierOptions

class Maestro:
    def __init__(self):
        self.model_path = './models//gesture_recognizer.task'
        
        sens_data = self.read_commands_config_file()["sensitivity"]
        self.options = GestureRecognizerOptions(
                base_options=BaseOptions(model_asset_path=self.model_path),
                running_mode=VisionRunningMode.LIVE_STREAM,
                result_callback=self.get_recognizer_result,
                num_hands = 1,
                min_hand_detection_confidence= sens_data["Detection_Sens"],
                min_hand_presence_confidence= sens_data["Presence_Sens"],
                min_tracking_confidence= sens_data["Tracking_Sens"],
                canned_gesture_classifier_options= ClassifierOptions(score_threshold= sens_data["Gesture_Recognizer_Sens"]))
        
        self.recognizer_result = None
        self.running = True
        
        
    def start_orchestra(self):
        '''
        Start the main program. Attempt to open the camera with OpenCV and receive the frames from it. If successful, format the frames for better 
        compatibility with mediapipe. Initialize the gesture recognition model, and attempt to execute the command if any gesture is recognized.
        '''
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            message = "Cannot open camera.\n"
            print(message)
            logging.error(message)
            exit()
            

        program_init_time = time.perf_counter()
        command_init_time = time.perf_counter()
        while self.running:
            
            read_response, frame = cap.read()
            if not read_response:
                message = "Can't receive frame. Exiting ...\n"
                print(message)
                logging.error(message)
                break
            
            frame = cv.flip(frame, 1)
            image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            
            with GestureRecognizer.create_from_options(self.options) as recognizer:
                recognizer.recognize_async(mp_image, self.get_elapsed_time_in_ms(program_init_time))
                
                try: 
                    gestures = self.recognizer_result.gestures
                    
                except AttributeError:
                    pass
                
                else:   
                    if not gestures == []:
                        gestures = self.recognizer_result.gestures
                        gesture_name = gestures[0][0].category_name
                        print(f"--[{gesture_name}]--")
                            
                        if self.check_command_cooldown(command_init_time, delay=1):
                            if self.execute_command_by_gesture(gesture_name):
                                command_init_time = time.perf_counter()

        cap.release()
        cv.destroyAllWindows()
        print("Program stopped.")
        
    
    def get_recognizer_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        # print('gesture recognition result: {}'.format(result))
        self.recognizer_result = result
        
        
    def execute_command_by_gesture(self, gesture_name):
        commands = self.read_commands_config_file()["commands"]
        
        if gesture_name in commands and commands[gesture_name] != "":
            threading.Thread(
                target=self.run_command_async, 
                args=(commands[gesture_name], gesture_name), 
                daemon=True
            ).start()   
                
            return True
        
    def run_command_async(self, cmd_str, g_name):
                env = os.environ.copy()
                try:
                    cmd = subprocess.Popen(cmd_str, 
                                    shell=True,
                                    start_new_session=True, 
                                    text=True,
                                    env=env,
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
                    
                    output, error = cmd.communicate()
                    
                    if error == "":
                        message = f"Executed: {cmd_str}\nUsing the gesture: {g_name}\nCommand output: {output or 'No output.'}\n"
                        logging.info(message)
                        print(message)
                    else:
                        message = f"The Shell detected an error: {cmd_str}\nGesture: {g_name}\nMessage: {error}\n"
                        logging.error(message)
                        print(message)
                        
                except Exception as e:
                    message = f"Python detected an error: {cmd_str}\nGesture: {g_name}\nMessage: {e}\n"
                    logging.error(message)
                    print(message)
            
            
    def read_commands_config_file(self) -> dict:
        if not os.path.exists("./config/config.json"):
            message = "No config file found. Please run the gui to configure the program.\n"
            print(message)
            logging.error(message)
            exit()
        
        with open("./config/config.json", "r") as config_file:
            return json.load(config_file)
        
    
    def check_command_cooldown(self, command_init_time, delay):
        current_time = time.perf_counter()
        if current_time >= command_init_time + delay:
            print("Cooldown Timed up : True")
            return True
        
        else:
            print("Cooldown Timed Up : False")
            return False


    def get_elapsed_time_in_ms (self, program_init_time):
        current_time = time.perf_counter()
        return int((program_init_time - current_time) * 1000)