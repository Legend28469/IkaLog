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

## IkaOutput_Slack: IkaLog Output Plugin for Slack
#
# Post game results to Slack, using Incoming Hook
class IkaOutput_Slack:

	##
	# Post a bot message to slack.
	# @param self     The Object Pointer.
	# @param text     Text message.
	# @param username Username.
	#
	def post(self, text = "", username = "＜8コ三"):
		try:
			import slackweb
			slack = slackweb.Slack(url = self.url)
			slack.notify(text = text, username = self.username)
		except:
			print("Slack: Failed to post a message to Slack")

	##
	# Generate a record for onGameIndividualResult.
	# @param self      The Object Pointer.
	# @param context   IkaLog context
	#
	def getTextGameIndividualResult(self, context):
		map = IkaUtils.map2text(context['game']['map'])
		rule = IkaUtils.rule2text(context['game']['rule'])
		won = IkaUtils.getWinLoseText(context['game']['won'], win_text ="勝ち", lose_text = "負け", unknown_text = "不明")
		return "%sで%sに%sました" % (map, rule, won)

	##
	# onGameIndividualResult Hook
	# @param self      The Object Pointer
	# @param context   IkaLog context
	#
	def onGameIndividualResult(self, context):
		s = self.getTextGameIndividualResult(context)

		fes_info = IkaUtils.playerTitle(IkaUtils.getMyEntryFromContext(context))
		if not fes_info is None:
			s = "%s (フェス %s)" % (s, fes_info)

		self.post(text = s, username = self.username)

	##
	# Check availability of modules this plugin depends on.
	# @param self      The Object Pointer.
	#
	def checkImport(self):
		try:
			import slackweb
		except:
			print("モジュール slackweb がロードできませんでした。 Slack 投稿ができません。")
			print("インストールするには以下のコマンドを利用してください。\n    pip install slackweb\n")

	##
	# Constructor
	# @param self     The Object Pointer.
	# @param url      Slack Incoming Hook Endpoint
	# @param username Name the bot use on Slack
	def __init__(self, url = None, username = "＜8ヨ"):
		self.url = url
		self.username = username
		self.checkImport()

if __name__ == "__main__":
	import sys
	obj = IkaOutput_Slack(
		url = sys.argv[1],
	)
	s = obj.getTextGameIndividualResult( {
			"game": {
				"map": {"name": "map_name"},
				"rule": {"name": "rule_name"},
				"won": True, }})
	print(s)
	obj.post(s)
