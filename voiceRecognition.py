import speech_recognition as sr
import subprocess

class speechTranslation:

    __MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"
    __device_id = None
    def __init__(self):

        # Set the device ID of the mic that we specifically want to use to avoid ambiguity
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if(microphone_name == self.__MIC_NAME):
                self.__device_id = i
                break
        
    def translateSpeech(self):
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone(device_index = self.__device_id) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)

            print("Start Speaking")
            try:
                audio = r.listen(source, timeout = 1.5)
            except sr.WaitTimeoutError:
                print("Listening timed out whilst waiting for phrase to start")
                return False

        # recognize speech using Google Speech Recognition
        try:
            return (r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return False
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return False


