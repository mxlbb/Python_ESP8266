import pymongo
import pandas as pd
import numpy as np
import streamlit as st


st.set_page_config(page_title=None, page_icon=None, layout="wide",
				   initial_sidebar_state="auto", menu_items=None)

dataMAC = "A8:48:FA:E7:2C:AD"
client = pymongo.MongoClient("mongodb://localhost:27017/")


with st.container():

	db = client["物联网"]["实时数据"]
	db_data = db.find_one({F"{dataMAC}.地址": dataMAC}, {"_id": 0})

	db_data_time = db_data[dataMAC]["时间"]
	db_data_Mac = db_data[dataMAC]["地址"]
	st.write("# 环境温度测试网页")

	col1, col3, col4, col5, col6, col7 = st.columns(6)

	col1.metric("气压强度", round(db_data[dataMAC]["气压强度"], 0), delta=None, delta_color="气压强度")
	# col2.metric("海拔高度", round(db_data[dataMAC]["海拔高度"], 2), delta=None, delta_color="海拔高度")
	col3.metric("摄氏温度", round(db_data[dataMAC]["摄氏温度"], 2), delta=None, delta_color="摄氏温度")
	col4.metric("华氏温度", round(db_data[dataMAC]["华氏温度"], 2), delta=None, delta_color="华氏温度")
	col5.metric("湿度数值", round(db_data[dataMAC]["湿度数值"], 2), delta=None, delta_color="湿度数值")
	col6.metric("光照强度", round(db_data[dataMAC]["光照强度"], 2), delta=None, delta_color="光照强度")
	col7.metric("紫外线强度", round(db_data[dataMAC]["紫外线强度"], 2), delta=None, delta_color="紫外线强度")

	db = client["物联网"]["统计数据"][dataMAC]
	db_data = db.find({}, {"_id": 0})
	db_data_gas = dict()
	# db_data_altitude = dict()
	db_data_celsius = dict()
	db_data_fahrenheit = dict()
	db_data_humidity = dict()
	db_data_light = dict()
	db_data_uv = dict()

	for f1 in db_data:
		db_data_gas.update({f1["时间"]: {"平均值": f1["平均值"]["气压强度"], "最大值": f1["最大值"]["气压强度"], "最小值": f1["最小值"]["气压强度"]}})
		# db_data_altitude.update({f1["时间"]: {"平均值": f1["平均值"]["海拔高度"], "最大值": f1["最大值"]["海拔高度"], "最小值": f1["最小值"]["海拔高度"]}})
		db_data_celsius.update({f1["时间"]: {"平均值": f1["平均值"]["摄氏温度"], "最大值": f1["最大值"]["摄氏温度"], "最小值": f1["最小值"]["摄氏温度"]}})
		db_data_fahrenheit.update({f1["时间"]: {"平均值": f1["平均值"]["华氏温度"], "最大值": f1["最大值"]["华氏温度"], "最小值": f1["最小值"]["华氏温度"]}})
		db_data_humidity.update({f1["时间"]: {"平均值": f1["平均值"]["湿度数值"], "最大值": f1["最大值"]["湿度数值"], "最小值": f1["最小值"]["湿度数值"]}})
		db_data_light.update({f1["时间"]: {"平均值": f1["平均值"]["光照强度"], "最大值": f1["最大值"]["光照强度"], "最小值": f1["最小值"]["光照强度"]}})
		db_data_uv.update({f1["时间"]: {"平均值": f1["平均值"]["紫外线强度"], "最大值": f1["最大值"]["紫外线强度"], "最小值": f1["最小值"]["紫外线强度"]}})
	# col1.write(db_data_gas)
	# col2.write(db_data_altitude)
	# col3.write(db_data_celsius)
	# col4.write(db_data_fahrenheit)
	# col5.write(db_data_humidity)
	# col6.write(db_data_light)
	# col7.write(db_data_uv)
	for f1k,f1v in db_data_gas.items():
		db_data_gas[f1k] = [int(f2) for f2 in f1v.values()]
	# for f1k,f1v in db_data_altitude.items():
	# 	db_data_altitude[f1k] = [int(f2) for f2 in f1v.values()]
	for f1k,f1v in db_data_celsius.items():
		db_data_celsius[f1k] = [int(f2) for f2 in f1v.values()]
	for f1k,f1v in db_data_fahrenheit.items():
		db_data_fahrenheit[f1k] = [int(f2) for f2 in f1v.values()]
	for f1k,f1v in db_data_humidity.items():
		db_data_humidity[f1k] = [int(f2) for f2 in f1v.values()]
	for f1k,f1v in db_data_light.items():
		db_data_light[f1k] = [int(f2) for f2 in f1v.values()]
	for f1k,f1v in db_data_uv.items():
		db_data_uv[f1k] = [int(f2) for f2 in f1v.values()]

	df1 = pd.DataFrame(list(db_data_gas.values()),columns=["平均","最大","最小"],index=list(db_data_gas))
	# df2 = pd.DataFrame(list(db_data_altitude.values()),columns=["平均","最大","最小"],index=list(db_data_altitude))
	df3 = pd.DataFrame(list(db_data_celsius.values()),columns=["平均","最大","最小"],index=list(db_data_celsius))
	df4 = pd.DataFrame(list(db_data_fahrenheit.values()),columns=["平均","最大","最小"],index=list(db_data_fahrenheit))
	df5 = pd.DataFrame(list(db_data_humidity.values()),columns=["平均","最大","最小"],index=list(db_data_humidity))
	df6 = pd.DataFrame(list(db_data_light.values()),columns=["平均","最大","最小"],index=list(db_data_light))
	df7 = pd.DataFrame(list(db_data_uv.values()),columns=["平均","最大","最小"],index=list(db_data_uv))
	col1.table(df1)
	# col2.table(df2)
	col3.table(df3)
	col4.table(df4)
	col5.table(df5)
	col6.table(df6)
	col7.table(df7)

	
	st.write(F"时间：{db_data_time}")
	st.write(F"MAC：{db_data_Mac}")