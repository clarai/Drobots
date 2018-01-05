#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
import socket
Ice.loadSlice('factory.ice --all -I .')
import drobots
Ice.loadSlice('container.ice --all -I .')
import Services

class PlayerI(drobots.Player):
	def __init__(self, broker):
		self.broker = broker
		self.counter = 1

	def makeController(self,robot, current=None):
		print("--------Creating the controllers--------")

		sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sckt.connect(("google.es",80))
		ip=sckt.getsockname()[0]
		sckt.close()

		if (self.counter == 4):
			self.counter = 1

		if(self.counter == 1):
			factory_prx = self.broker.stringToProxy("factory -t -e 1.1:tcp -h {} -p 6062 -t 60000".format(ip))
		elif(self.counter == 2):
			factory_prx = self.broker.stringToProxy("factory -t -e 1.1:tcp -h {} -p 6063 -t 60000".format(ip))
		else:
			factory_prx = self.broker.stringToProxy("factory -t -e 1.1:tcp -h {} -p 6064 -t 60000".format(ip))
		self.counter += 1
		print(factory_prx)

		factory = drobots.RobotControllerFactoryPrx.checkedCast(factory_prx)


		robots_container_prx = self.broker.stringToProxy("container -t -e 1.1:tcp -h {} -p 6061 -t 60000".format(ip))
		robots_container = Services.ContainerPrx.checkedCast(robots_container_prx)

		robot_identity = len(robots_container.list())

		robot_prx = factory.make(robot, robot_identity)

		robots_container.link(robot_identity, robot_prx)

		return robot_prx

	def win(self, current=None):
		print("--------YOU WIN, CONGRATULATIONS!!--------")
		current.adapter.getCommunicator().shutdown()

	def lose(self, current=None):
		print("--------YOU LOSE, GOOD LUCK NEXT TIME!!--------")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current=None):
		print("--------GAME ABORTED--------")
		current.adapter.getCommunicator().shutdown()

class PlayerApp(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		adapter = broker.createObjectAdapter("PlayerAdapter")
		adapter.activate()

		game_prx = drobots.GamePrx.checkedCast(broker.stringToProxy(argv[1]))

		servant = PlayerI(broker)

		player_prx = drobots.PlayerPrx.uncheckedCast(adapter.createDirectProxy
			(adapter.addWithUUID(servant).ice_getIdentity()))

		nick = argv[2]

		try:
			game_prx.login(player_prx, nick)
			print("--------You've loged in--------")
			print("In the server {} with the nick {}".format(argv[1], argv[2]))

		except drobots.GameInProgress:
			print("--------GAME IN PROGRESS - TRY AGAIN LATER--------")
			return 1
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0


player = PlayerApp()
sys.exit(player.main(sys.argv))