from pathlib import Path
import threading
import time
import pyaudio
import wave
import numpy as np
from argparse import ArgumentParser


class SoundControlValue:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pyaudio.PyAudio()
    frames = []
    value_up = 2
    is_recording = True
    time_recording = round(time.time())

    def set_filename(self, file_name="output2.wav"):
        self.WAVE_OUTPUT_FILENAME = file_name

    def check_path(self, path_):
        path_ = '/'.join(str(path_).replace('\\', '/').split('/')[:-1])
        if path_:
            Path(path_).mkdir(parents=True, exist_ok=True)
        print(f'Dir path "{path_}" checked')

    def init_stream(self):

        if not self.WAVE_OUTPUT_FILENAME:
            self.set_filename()

        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True, output=True,
                                  frames_per_buffer=self.CHUNK)

    def set_value_up(self, val=2):
        self.value_up = val

    def stop_stream(self):

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def start_stream(self):
        print("* start recording")

        while self.is_recording:
            data = self.stream.read(self.CHUNK)
            data_g = np.frombuffer(data, dtype=np.int16)

            data_g = data_g * self.value_up
            data_g = bytes(data_g)
            self.stream.write(data_g)
            self.frames.append(data_g)

        print("* done recording")
        self.stop_stream()

        print(f'time of recording {round(time.time()) - self.time_recording} second')
        self.write_to_file()

    def write_to_file(self):

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print('Writed to file')


class WorkerSound:
    sound = SoundControlValue()

    def time_out(self):
        time.sleep(60)
        self.sound.is_recording = False
        self.t1.join()
        self.t3.join()
        self.t2.join()

    def wait_key(self):
        time.sleep(1)
        while True:
            a = input('Enter q for stop recording: \n')
            if a == 'q':
                break

        delta_time = 5 - (round(time.time()) - self.sound.time_recording)
        if delta_time > 0:
            time.sleep(delta_time)
        self.sound.is_recording = False
        self.t1.join()

    def args_validate(self, args_):

        args_.volume = args_.volume if args_.volume >= 1 else 1
        args_.volume = args_.volume if args_.volume <= 5 else 5

        args_.filepath = args_.filepath if '.wav' in args_.filepath else 'output.wav'

        return args

    def __init__(self, args_):
        args_ = self.args_validate(args_)

        self.t1 = threading.Thread(target=self.recorder, args=(args_,), daemon=True)
        self.t2 = threading.Thread(target=self.wait_key, daemon=True)
        self.t3 = threading.Thread(target=self.time_out, daemon=True)

        self.t1.start()
        self.t2.start()
        self.t3.start()

        self.t1.join()

    def recorder(self, args):

        self.sound.set_value_up(args.volume)
        self.sound.check_path(args.filepath)
        self.sound.set_filename(args.filepath)
        self.sound.init_stream()
        self.sound.start_stream()


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-p", "--file", dest="filepath",
                        help="write record to FILE", metavar="FILE")

    parser.add_argument("-v", "--volume", dest="volume",
                        help="volume growUp", default=2, type=int)
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")

    args = parser.parse_args()
    if args.filepath and args.volume:
        WorkerSound(args)
    else:
        print('please rerun program with comand\n-p <path to file>\n-v <value grow up volume>')
