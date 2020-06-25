import requests
from matplotlib import pyplot as plt


def getData():
    #자료 출처: coronaboard.kr
    url = "https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_daily.csv"
    response = requests.get(url)
    return response.text


def getCsvData(data):
    ret = data.split("\n")
    count = len(ret)
    day = []
    confirmedStack = []
    releasedStack = []
    for i in range(count - 9, count):  # 전체 데이터에서 지난 8일간 누적된 데이터 출력
        csvData = ret[i]  # 1일동안 누적된 데이터값. ex) 20200616,12155,278,10760...
        csvSplit = csvData.split(",")
        key = csvSplit[0]
        key = key[4:]  # 연도 분리
        conf = csvSplit[1]
        rel = csvSplit[3]
        day.append(key)  #날짜 정보는 그대로 string으로 append
        confirmedStack.append(int(conf))
        releasedStack.append(int(rel))
    # 데이터가 확진자/완치자가 누적된 형태로 제공되므로, 데이터를 일일 확진자 수로 변환해야함.
    confirmed = []
    released = []
    for i in range(1, len(confirmedStack)):
        # releasedStack과 confirmedStack의 크기가 동일하므로 한번에 처리.
        confirmed.append(confirmedStack[i] - confirmedStack[i - 1])
        released.append(releasedStack[i] - releasedStack[i - 1])
    # day는 8일간의 데이터를 포함하므로 맨 첫번째 날짜 삭제
    del day[0]
    return {"day": day, "confirmed": confirmed, "released": released}


def plot(data):
    print(data)
    plt.title("Corona19 ")
    plt.xlabel("Date")
    plt.ylabel("Confirmed, Released")
    plt.plot(data["day"], data["confirmed"], "ro--")
    plt.plot(data["day"], data["released"], "go-")
    plt.show()


data = getData()
csvData = getCsvData(data)
plot(csvData)
