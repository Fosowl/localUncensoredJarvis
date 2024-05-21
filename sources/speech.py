from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import subprocess

class Speech():
    def __init__(self) -> None:
        self.model = VitsModel.from_pretrained("facebook/mms-tts-eng")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

    def speak(self, sentence):
        for chunk in sentence.split('.'):
            if len(chunk) < 16:
                continue
            try:
                inputs = self.tokenizer(chunk, return_tensors="pt")
                with torch.no_grad():
                    output = self.model(**inputs).waveform
                scipy.io.wavfile.write("./voice.wav", rate=self.model.config.sampling_rate, data=output.float().numpy().T)
                audio_file = "./voice.wav"
                return_code = subprocess.call(["afplay", audio_file])
            except Exception as e:
                print("Error with text2speech module.\n" + str(e))

if __name__ == "__main__":
    speech = Speech()
    speech.speak("hello would you like coffee ?")
