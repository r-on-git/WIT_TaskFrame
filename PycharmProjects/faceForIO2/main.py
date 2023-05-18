# This is a sample Python script.
import Interface
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import OpenCvStream




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
        # interface = Interface.Interface()
        # interface.mainloop()
        region='rightEyebrow'
        stream = OpenCvStream.OpenCvStream(region)  # create an instance of the openCvStream class
        stream.readCamera(region)  # call the readCamera method on the instance

#TODO: make the selected face area as parameter/ split read camera further
#try calling mediapipepart functions here , outside of read camera/ make a sub function to call these within readcamera, but from here.
# consider where and how it runs smoothest, as currently there are some lags, probably due to too many unnecessary calls and prints

'''
    stream = openCvStream()  # create an instance of the openCvStream class
    stream.readCamera()  # call the readCamera method on the instance

'''


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
