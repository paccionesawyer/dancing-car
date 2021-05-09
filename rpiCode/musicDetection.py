"""
Sawyer Bailey Paccione and Olif Soboka Hordofa
audioDetection.py
Tufts University Spring 2021, ME-0035
Purpose:        Detect whether audio was playing or not playing and convey that 
                information to a LEGO SPIKE PRIME
Description:    This audio detection uses K-Nearest-Neighbors Algorithm. This
                is a supervised training algorithm. There are two cases, no music, and music. 
                1. Have no music playing and read in 5 Values
                2. Play music and read in another 5 Values
                3. Run the microphone continuously and get the most recent 
                   reading
                4. Find the minimum distance between this reading and the 5 no 
                   music values and the 5 music values. 
                5. Send the case (music/no-music) for the value that has the 
                   minimum distance to the SPIKE PRIME
"""

################################################################################
#                                   Imports                                    #
################################################################################
import serial, time # Serial Communication to The Spike Prime
import pyaudio, wave # Essential for Audio Detection

from array import array # Mathematics for Audio Processing
import statistics


################################################################################
#                        Setup for Serial Communication                        #
################################################################################
serialPort = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


################################################################################
#                               Setup for Audio                                #
################################################################################
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 1 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)

audio = pyaudio.PyAudio() # create pyaudio instantiation

"""
    get_audio_val()
Purpose:    Read a value from the microphone attached to the RPI 
Arguments:  N/A
Returns:    The Average of the all the readings taken in 1 second
Effects:    N/A
Notes:      Everytime that this function is called the PyAudio object
            is opened and closed. This appears inefficient; however it works
            and if simply opened at the beggining of the program and closed
            at the end, there is an overflow error.
"""
def get_audio_val() :
    # Start Listening For Audio
    stream = audio.open(format = form_1, \
                    rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        raw = stream.read(chunk)
        data = array('h',raw).tolist()
        std = statistics.stdev(data)
        frames.append(std)
    audio.close(stream)

    # Calculate the Average reading of the Audio Data
    mu = statistics.mean(frames)

    print("Mu:", mu)

    return mu


################################################################################
#                               Global Variables                               #
################################################################################
training = []
# class_training = [[0, 1335.4445504225775], [0, 1356.6027573564102], [0, 1249.9147047388728], [0, 1511.3257309542355], [0, 1281.1382817982096], [1, 1780.7345239511874], [1, 2416.3177562886126], [1, 1774.6496247911393], [1, 1631.1579184233392], [1, 1809.1426950083303]] # Uncomment if you don't want to do training

"""
    train_nearest_neighbors()
Purpose:    Train kNN Algorithm for Music Detection 
Arguments:  N/A
Returns:    N/A
Effects:    Initializes the values in training array
Notes:      Waits for user input to continue reading the next value
"""
def train_nearest_neighbors():
    for case in range(2) :
        for counter in range(5):
            command_string = "Press Enter To get the " + str(counter + 1) + " value for case " + str(case + 1) + " "
            input(command_string)
            sound = get_audio_val()
            training.append([case, sound])
            time.sleep(0.1)

    print(training)

"""
    main()
Purpose:    Runs the main computer program of Audio Dection
Arguments:  N/A
Returns:    N/A
Effects:    Training Array and the Serial Port connected to the SPIKE PRIME
Notes:      
"""
def main() :
    train_nearest_neighbors()
    curr_case = 0
    while True:
        curr_sound = get_audio_val()
        mini = 1000
        prev_case = curr_case
        for (c,s) in training:
            dist = abs(curr_sound - s)
            if dist < mini:
                mini = dist
                curr_case = c
        if (curr_case != prev_case) :
            # Send Case to Spike if Different then before
            print(curr_case)
            if serialPort:
                to_send = str(curr_case) + "\r\n"
                serialPort.write(to_send.encode())

if __name__ == "__main__":
    main()
