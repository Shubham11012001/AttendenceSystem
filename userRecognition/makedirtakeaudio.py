import os,pyaudio,wave,shutil
from . import test


def makeDirector(username01):
    print("I am here")
    x = username01
    print(x)
    final = "userRecognition/trainingData/"+x
    try:
        os.mkdir(final)
    except OSError as error:
        print(error)
        
def movefile(file,destination):
    source = file
    shutil.move(source, destination) 

def recordaudio(username01,i):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    username = username01
    filename = "userRecognition/trainingData/"+username+"/"+username+str(i)+".wav"
    WAVE_OUTPUT_FILENAME = filename
    
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    textfile = "userRecognition/textFiles/"+username+".txt"
    f = open(textfile, "a")
    x = filename+"\n"
    f.write(x)
    f.close()
    #movefile(filename,username)



def testing_recordaudio(username01):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    username = username01
    filename = "userRecognition/testing_audios/"+username+".wav"
    WAVE_OUTPUT_FILENAME = filename
    
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    return (test.testing_recorded_audio(filename))





