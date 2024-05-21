from colorama import Fore
import pyaudio
import os
import wave
import shutil

# RECORD
wav_path = "./record.wav"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8192
RECORD_SECONDS = 7

def get_microphone(wf, stream):
    frames = []
    count = 0
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = bytes(0)
        try:
            data = stream.read(CHUNK)
            count += 1
        except:
            print("Subprocess: Failed to read stream.")
            pass
        frames.append(data)
    wf.writeframes(b''.join(frames))
    return wf

done = False

def get_recording(audio, verbose=False):
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)
    if verbose: print("Subprocess: Recording...")
    while not done:
        wf = wave.open('./tmp.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf = get_microphone(wf, stream)
        try:
            shutil.copy('./tmp.wav', './record.wav')
            os.remove('./tmp.wav')
        except Exception as e:
            if verbose: print("Subprocess: Failed to copy tmp file.")
            pass
        wf.close()
    stream.stop_stream()
    stream.close()

def main():
    audio = pyaudio.PyAudio()
    try:
        # cleanup
        os.remove('./tmp.wav')
        os.remove('./record.wav')
    except:
        pass
    get_recording(audio)
    audio.terminate()

main()
