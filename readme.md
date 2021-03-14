#Sound volume increate 

For start \
Install Python 3.7 

##INSTALL
install libs \
numpy\
PyAudio

if not install \
go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio \
download 'PyAudio-0.2.11-cp37-cp37m-win_amd64.whl' to project dir\
pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl\
or search actual version

##RUN programm

python recording_audio.py -p <path> -v <volume> \
<path> is file path only .wav format or replace path on output.wav \
<volume> is volume of increate sound range 1-5

comand like \
python recording_audio.py -p dir/output.wav -v 4

Programm recording 60 second \
If you want create short record need enter <q> in console \
And program break of recording


