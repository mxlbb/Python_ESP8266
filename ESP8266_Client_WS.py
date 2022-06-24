import json
import time
import asyncio
import pymongo
import datetime
import websockets


async def WS(dataMAC, dataIP, dataMSG):
	async with websockets.connect(dataIP) as websocket:
		client = pymongo.MongoClient("mongodb://localhost:27017/")
		await websocket.recv()
		while True:
			await websocket.send(dataMSG)
			dataJson = dict()
			dataJson.update({"时间": str(datetime.datetime.now())[:-7], "地址": dataMAC})
			dataJson.update(json.loads(await websocket.recv()))
			db = client["物联网"]["实时数据"]
			db.update_one({F"{dataMAC}.地址": dataMAC}, {"$set": {dataMAC: dataJson}}, True)
			# if(dataJson["状态"] == False):
			#     db.update_one({F"{dataMAC}.状态": False}, {"$set": {dataMAC: dataJson}}, True)
			# if(dataJson["状态"] == True):
			#     db.update_one({F"{dataMAC}.状态": True}, {"$set": {dataMAC: dataJson}}, True)

			if(int(datetime.datetime.now().timestamp()) % 2 == 0):
				dbs = client["物联网"]["历史数据"][dataMAC]
				dbt = client["物联网"]["统计数据"][dataMAC]
				dbs.insert_one(dataJson)
				del dataJson["_id"]
				time.sleep(0.5)
				##################################################
				dbs = dbs.find({F"时间": {"$regex": str(datetime.datetime.now())[:-10]}}, {"_id": 0})
				dbs = list(dbs)
				dbs_max = dict()
				dbs_min = dict()
				dbs_average = dict()
				for f1 in dbs:
					for f2k, f2v in f1.items():
						if(f2k not in list(dbs_max) or f2v > dbs_max[f2k]):
							dbs_max[f2k] = f2v
						if(f2k not in list(dbs_min) or f2v < dbs_min[f2k]):
							dbs_min[f2k] = f2v
						dbs_average.update({f2k: f2v + dbs_average[f2k] if f2k in list(dbs_average) else f2v})
				dbs = len(dbs)
				'''
				下面的状态指在线率
				'''
				for f1k, f1v in dbs_average.items():
					if(type(f1v) != str):
						dbs_average.update({f1k: round(f1v / dbs, 2)})
					else:
						dbs_average.update(
							{f1k: str(datetime.datetime.now())[:-7]})

				dbs_average.update({"地址": dataMAC}) # 修复平均时->地址出现时间问题

				# 设置时间"时间": str(datetime.datetime.now())[:-10]
				dbs = {"时间": str(datetime.datetime.now())[:-10], "最大值": dbs_max, "最小值": dbs_min, "平均值": dbs_average}
				dbt.update_one({F"时间": str(datetime.datetime.now())[:-10]}, {"$set": dbs}, True)
				##################################################
		client.close()

mac = "A8:48:FA:E7:2C:AD"
ip = "ws://[fe80::aa48:faff:fee7:2cad]:80"
msg = "环境数据"

asyncio.run(WS(mac, ip, msg))
