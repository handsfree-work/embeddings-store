import os

os.environ.setdefault("HTTPS_PROXY", "http://192.168.34.139:10811")
#os.system("python -m pip install -r requirements.txt -i https://pypi.douban.com/simple/")
os.system("python -m pip install -r requirements.txt")
