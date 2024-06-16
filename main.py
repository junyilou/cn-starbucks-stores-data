import json
import os
from dataclasses import asdict
from datetime import datetime
from json import loads
from urllib.request import build_opener
from zoneinfo import ZoneInfo

from models import DataDict, Store, parse

API_URL = "https://www.starbucks.com.cn/api/stores"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"

def main() -> None:
	LOCAL_TIME = datetime.now().astimezone()
	BEIJING_TIME = LOCAL_TIME.astimezone(ZoneInfo("Asia/Shanghai"))

	with open("stores.json", "r") as r:
		j = json.load(r)
	print(f"[本地文件] {j["meta"]["update"]}")
	saved = [Store(**d) for d in j["data"]]

	print(f"[下载文件] {BEIJING_TIME:%F %T}")
	opener = build_opener()
	opener.addheaders = [("User-Agent", USER_AGENT)]
	with opener.open(API_URL) as response:
		j: DataDict = loads(response.read())
	print(f"[解析文件] {j["meta"]["total"]} 家门店")

	assert j["data"], "门店信息为空"

	stores = sorted(parse(s) for s in j["data"])
	if saved == stores:
		return print(f"[提前结束] 文件无差异")

	dumps = {"meta": {"total": j["meta"]["total"],
		"update": BEIJING_TIME.strftime("%F %T")},
		"data": [asdict(s) for s in stores]}
	print(f"[生成文件] {stores[0].id}...{stores[-1].id}")

	with open("stores.json", "w") as w:
		json.dump(dumps, w, ensure_ascii = False, indent = 2)
	with open(os.environ["GITHUB_ENV"], "a") as w:
		w.write("SHOULD_COMMIT=true")

if __name__ == "__main__":
	raise SystemExit(main())