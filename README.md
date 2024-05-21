# localUncensoredJarvis
Like gpt4o but slower and wilder, running locally using ollama and a bunch of hugging-face models.

this readme will be improved..

## Install

- Make sure you have ollama installed on your machine
- Install dependencies (`pip3 install -r requirements.txt`)

## Run

- In first terminal run `ollama serve`
- In second terminal run `sudo python3 main.py` (sudo is required on some machine)
- Ollama will download `llama2-uncensored` on your machine and 2 small hugging-face model (`facebook/mms-tts-eng` and `distil-whisper/distil-medium.en`).
- Add `--deaf` if you want to type instead of talking.
- type or say goodbye to exit.

NOTE: you may have to run `./repair.sh` if the script is stuck on "waiting for subprocess", this due to the fact that a subprocess python script is needed to continuously listen to microphone, and it may get detached if program does not properly exit. (totally should be fixed i know)

## Usage

You have to say one of the following word for the microphone recording to be send to the LLM "understood", "thanks" or "do it".
You can reset the interpreted transcription text by voice by saying "I mean", "I am saying", "reset", "I mean to say".
You can exit by saying "goodbye"

## Current capabilities

- Understand what you say
- Python code execution
- Using bash to interact to do anything.
- Get feedback from python/bash interpreter and fix error by itself
- Speak with a cool voice.
- Will pretty much do anything you ask. 
