#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  IkaLog
#  ======
#  Copyright (C) 2015 Takeshi HASEGAWA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from IkaUtils import *

from datetime import datetime
import time
import json

## IkaOutput_CSV: IkaLog Output Plugin for CSV Logging
#
# Write JSON Log file
class IkaOutput_JSON:

	##
	# Write a line to text file.
	# @param self     The Object Pointer.
	# @param record   Record (text)
	#
	def writeRecord(self, record):
		try:
			json_file = open(self.json_filename, "a")
			json_file.write(record)
			json_file.close
		except:
			print("JSON: Failed to write JSON file")

	##
	# Generate a record for onGameIndividualResult.
	# @param self      The Object Pointer.
	# @param context   IkaLog context
	#
	def getRecordGameIndividualResult(self, context):
		map = IkaUtils.map2text(context['game']['map'])
		rule = IkaUtils.rule2text(context['game']['rule'])
		won = IkaUtils.getWinLoseText(context['game']['won'], win_text ="win", lose_text = "lose", unknown_text = "unknown")

		t = datetime.now()
		t_str = t.strftime("%Y,%m,%d,%H,%M")
		t_unix = int(time.mktime(t.timetuple()))

		record = { 'time': t_unix, 'event': 'GameResult', 'map': map, 'rule': rule, 'result': won }
		return json.dumps(record, separators=(',',':'))

	##
	# onGameIndividualResult Hook
	# @param self      The Object Pointer
	# @param context   IkaLog context
	#
	def onGameIndividualResult(self, context):
		record = self.getRecordGameIndividualResult(context)
		self.writeRecord(record)

	##
	# Constructor
	# @param self          The Object Pointer.
	# @param json_filename JSON log file name
	#
	def __init__(self, json_filename):
		self.json_filename = json_filename
