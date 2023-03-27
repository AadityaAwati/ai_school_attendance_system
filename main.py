from pyzbar.pyzbar import decode
import PIL
import requests
import cv2
import numpy as np
import imutils
import datetime
import time
import pandas

url = input("Enter the url: ")

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)

    for barcode in decode(img):
        time_ = datetime.datetime.now().strftime("%H:%M")
        time_split = time_.split(":")
        complete_time = datetime.datetime(hour=int(time_split[0]), minute=int(time_split[1]), day=datetime.datetime.now().day, month=datetime.datetime.now().month, year=datetime.datetime.now().year)
        required_time = datetime.datetime(hour=8, minute=15, day=datetime.datetime.now().day, month=datetime.datetime.now().month, year=datetime.datetime.now().year)
        with open("data.csv") as data_file:
            data = pandas.read_csv(data_file)
        data_dict = data.to_dict()
        names = [name for name in data_dict["name"].values()]
        data_ = barcode.data.decode().split(",")

        if data_dict["name"] == {}:
            data_dict["name"]["0"] = data_[0]
            data_dict["class"]["0"] = data_[1]
            data_dict["roll number"]["0"] = data_[2]
            data_dict["time"]["0"] = time_
            data_dict["late"]["0"] = complete_time > required_time
            dataframe = pandas.DataFrame(data_dict)
            dataframe = dataframe.loc[:, ~dataframe.columns.str.match('Unnamed')]
            dataframe.to_csv("data.csv", index=False)
        elif names[len(names) - 1] != data_[0]:
            data_dict["name"]["0"] = data_[0]
            data_dict["class"]["0"] = data_[1]
            data_dict["roll number"]["0"] = data_[2]
            data_dict["time"]["0"] = time_
            data_dict["late"]["0"] = complete_time > required_time
            print(data_[0], data_[1], data_[2])
            dataframe = pandas.DataFrame(data_dict)
            dataframe = dataframe.loc[:, ~dataframe.columns.str.match('Unnamed')]
            dataframe.to_csv("data.csv", index=False)

    cv2.imshow("Camera Footage", img)

    if cv2.waitKey(1) == ord("q"):
        break
cv2.destroyAllWindows()
time.sleep(3)
