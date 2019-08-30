from aip import AipOcr
def ocr_pic():
    """ 你的 APPID AK SK """
    APP_ID = 'xxxxxx'
    API_KEY = 'xxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxx'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content('1.png')

    """ 调用通用文字识别, 图片参数为本地图片 """
    client.basicGeneral(image)

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    res = client.basicGeneral(image, options)['words_result'][0]['words']
    return res

# print(res)
# url = "http//www.x.com/sample.jpg"

# """ 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url)

# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"

# """ 带参数调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url, options)

