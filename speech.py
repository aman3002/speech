import speech_recognition as sr
import pyaudio
import os
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pyttsx3 as p
r=sr.Recognizer()
print("MAIN MENU ")
print("enter 1 to convert voice to text")
print("enter 2 to convert wav file to text")
print("enter 3 to convert text file to speech")
print("enter 4 to text to speech")
choice=int(input("enter your choice"))
if choice==1:
  data=''
  r = sr.Recognizer()
  with sr.Microphone(2) as source:
    print("Say something!")
    audio = r.listen(source)
  try:
    print("You said: " + r.recognize_google(audio))
    print("stop")
  except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
elif choice==2:
  def get_large_audio_transcription(path):
    sound=AudioSegment.from_wav(path)
    chunks=split_on_silence(sound,min_silence_len= 500,silence_thresh=sound.dBFS-14,keep_silence=500)
    folder_name="audio-chunks"
    if not os.path.isdir(folder_name):
      os.mkdir(folder_name)
    whole_text=""
    for i,audio_chunk in enumerate(chunks,start=1):
      chunk_filename=os.path.join(f"chunk{i}.wav")
      audio_chunk.export(chunk_filename,format="wav")
      with sr.AudioFile(chunk_filename) as source :
        audio_listened=r.record(source)
        try:
          text=r.recognize_google(audio_listened)
        except sr.unknownvalueerror as e:
          print("error:",str(e))
        else:
          text=f"{text.capitalize()}."
          print(chunk_filename,":",text)
          whole_text+=text
    return whole_text
  path=input("enter the path of the .wav file")
  get_large_audio_transcription(path)
elif choice==3:
  engine=p.init()
  f=input("please enter the name of the file with path")
  file=open(f,"r")
  fi=file.read()
  engine.say(fi)
  engine.runAndWait(2)
  file.close()
elif choice==4:
  engine=p.init()
  f=input("enter the text")
  engine.say(f)
  engine.runAndWait()
else:
  print("you enter invalid input")
