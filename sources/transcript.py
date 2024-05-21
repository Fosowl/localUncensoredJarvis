
from colorama import Fore
import os
import time

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

CONFIRM_WORDS = ["understood", "thanks", "do it"]
RESET_WORDS = ["reset", "I repeat", "nevermind", "I said", "I mean", "I am saying", "I am saying", "I'm saying", "hey" "I am back", "wake up"]
STOP_KEYWORDS = ["goodbye", "ciao", "au revoir", "quit", "exit", "leave", "terminate", "shut down", "shut-down", "shut down", "power off", "power-off", "poweroff", "abort"]

class Transcript():
    def __init__(self) -> None:
        self.last_read = None
        self.wav_path = "./record.wav"
        if os.path.exists(self.wav_path):
            os.remove(self.wav_path)
        device = "cuda:0" if torch.cuda.is_available() else "mps"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model_id = "distil-whisper/distil-medium.en"
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(model_id)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            torch_dtype=torch_dtype,
            device=device,
        )

    def contain(self, sequence, keywords) -> bool:
        for key in keywords:
            if key.lower() in sequence.lower():
                return True
        return False

    def is_file_bad(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                return len(f.read()) < 1024
        except FileNotFoundError:
            return True

    def is_file_same(self):
        try:
            with open(self.wav_path, 'rb') as f:
                data = f.read()
                self.last_read = data
                return data == self.last_read
        except FileNotFoundError:
            return False

    """
    # For speechomatics api mode
    def script2text(self, USE_MIC):
        file_path = './testing/script.txt'
        while True:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    text = f.read().strip()
                    if len(text) > 0:
                        os.remove(file_path)
                        break
        print("Understand:", text)
        return text
    """

    def transcript_job(self):
        result = self.pipe(self.wav_path)
        return result["text"]

    def speech2textWhisper(self, USE_MIC):
        transcript = ""
        done = False
        last_transcript = ""
        while not done:
            if self.is_file_bad(self.wav_path):
                print(Fore.YELLOW, "waiting for subprocess", Fore.WHITE)
                time.sleep(1)
                continue
            start_listen_time = time.time()
            whisper_interpretation = self.transcript_job()
            if whisper_interpretation == last_transcript:
                continue
            last_transcript = whisper_interpretation
            end_listen_time = time.time()
            comprehension_time = round(end_listen_time - start_listen_time, 1)
            print(Fore.LIGHTBLACK_EX, f"Understand : {whisper_interpretation} ({comprehension_time} s)")
            transcript += whisper_interpretation
            if self.contain(whisper_interpretation.lower(), CONFIRM_WORDS):
                done = True
            if self.contain(whisper_interpretation.lower(), STOP_KEYWORDS):
                done = True
                return "stop"
            if self.contain(whisper_interpretation.lower(), RESET_WORDS):
                print(Fore.YELLOW, "Waiting for reformulated query")
                transcript = ""
        return transcript
