#!/usr/bin python3

import sys
import time
from colorama import Fore
import signal
import argparse
import subprocess

from sources.transcript import Transcript
from sources.speech import Speech
from sources.model import Model

parser = argparse.ArgumentParser(description='Jarvis, an AI assistant')
parser.add_argument('--silent', action='store_true',
                help='Prevent AI from speaking, only display answer')
parser.add_argument('--deaf', action='store_true',
                help='Do not listen to user, use text input instead')
args = parser.parse_args()

REPLY_COLOR_TEXT = Fore.LIGHTCYAN_EX
REPLY_COLOR_CODE = Fore.LIGHTBLUE_EX
ENTRY_COLOR = Fore.LIGHTGREEN_EX
VOICE_ACTIVE = not args.silent
USE_MIC = not args.deaf

mic_process = None

def get_user_query(transcripter) -> str:
    if USE_MIC == True:
        print(ENTRY_COLOR + f">>> Listening... <<<", Fore.RESET)
        return transcripter.speech2textWhisper(USE_MIC)
    else:
        buffer = ""
        while buffer == "" or buffer.isascii() == False:
            buffer = input(ENTRY_COLOR + f">>> " + Fore.RESET)
        return buffer

def conversation_loop():
    transcripter = Transcript()
    speech = Speech()
    model = Model("llama2-uncensored")
    while True:
        user = get_user_query(transcripter)
        if user == "stop":
            print("Goodbye!")
            break
        answer = model.answer(user, speech)
        print(REPLY_COLOR_TEXT, answer, Fore.RESET)
        if VOICE_ACTIVE:
            speech.speak(answer)

interupt_request = 0
def handleInterrupt(signum, frame):
    global mic_process
    global interupt_request
    mic_process.terminate()
    if interupt_request >= 2:
        print(Fore.YELLOW + "Program aborted by user.")
        sys.exit(1)
    else:
        interupt_request += 1

def main():
    global mic_process
    mic_process = subprocess.Popen(["python3", "./sources/microphone/start_mic2wav.py"])
    time.sleep(1)
    signal.signal(signal.SIGINT, handler=handleInterrupt)
    conversation_loop()
    mic_process.terminate()

if __name__ == "__main__":
    main()
