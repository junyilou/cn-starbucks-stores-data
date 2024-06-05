import json
from dataclasses import asdict
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from models import DataDict, parse

API_URL = "https://www.starbucks.com.cn/api/stores"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"

def main() -> None:
	LOCAL_TIME = datetime.now().astimezone()
	BEIJING_TIME = LOCAL_TIME.astimezone(ZoneInfo("Asia/Shanghai"))

	print(f"[下载文件] {BEIJING_TIME:%y%m%d-%H%M%S}")
	r = requests.get(API_URL, headers = {"User-Agent": USER_AGENT})
	j: DataDict = r.json()
	print(f"[解析文件] {j["meta"]["total"]} 家门店")

	assert j["data"], "门店信息为空"

	stores = sorted(parse(s) for s in j["data"])
	dumps = {"meta": {"total": j["meta"]["total"],
		"update": BEIJING_TIME.strftime("%F %T")},
		"data": [asdict(s) for s in stores]}

	print(f"[生成文件] {stores[0].id}...{stores[-1].id}")
	with open("stores.json", "w") as w:
		json.dump(dumps, w, ensure_ascii = False, indent = 2)

if __name__ == "__main__":
	raise SystemExit(main())