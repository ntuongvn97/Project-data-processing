import urllib.request as urllib
import os
from bs4 import BeautifulSoup
from pprint import pprint
import cv2
import json
global old_video
old_video = None


def get_info(id, base_path):
    global old_video
    quote_page = "http://camera.centic.vn/chitiet/index/{:d}".format(id)
    page = urllib.urlopen(quote_page)
    soup = BeautifulSoup(page, "html.parser")
    try:
        url_video = "http://camera.centic.vn" + soup.video.get("src")
        if soup.video.get("src") == "/" or url_video == old_video:
            return None
        table = soup.tbody.find_all("td")
        cap = cv2.VideoCapture(url_video)
    except Exception as e:
        print(e)
        return None

    time = table[0].string.replace(" ", "").replace("-", "").replace(":", "")

    if table[1].string == "Quốc lộ 14B - UBND Hòa Vang":
        location = "QL"
    else:
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        cap.release()
        if w == 1280:
            location = "TNV"
        elif w == 2048:
            location = "NT"
        else:
            location = "unknow"
    status = "morning" if 6 <= int(time[8:10]) < 18 else "evening"
    path = "{}{}/{}/{}.mp4".format(base_path, location, status, str(id))
    data = {
        "id": id,
        "video": url_video,
        "time": time,
        "status": status,
        "location": location,
        "path": path,
    }
    old_video = url_video
    return data


if __name__ == "__main__":
    # index = 545761
    # index = 545530
    # index = 545504
    # index = 544005
    index = 627000
    base_path = "Centic/Video/"
    datas = []
    data = get_info(index, base_path)
    pprint(data)
    # if data is None:
    #     index -= 1
    #     break
    # else:
    #     try:
    #         datas.index(data)
    #         print("Video is exits")
    #         break
    #     except ValueError:
    #         print(data)
    # try:
    #     urllib.urlretrieve(data["video"], data["path"])
    # except Exception as e:
    #     print("-- >", e)
    #     break
    # datas.append(data)
    # index -= 1
    # f = open("data.json", "w")
    # json.dump(datas, f)
    # f.close()
