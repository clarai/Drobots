import Ice
import sys
Ice.loadSlice('factory.ice --all -I .')
Ice.loadSlice('container.ice --all -I .')
import drobots
import Services
import socket




class RobotControllerFactoryI(drobots.RobotControllerFactory):
	def make(self, robot, identifier, current=None):
		if(robot.ice_isA("::drobots::Attacker")):
			print("----Creating Attacker Controller----")
			servant = RobotControllerAttackerI(robot, identifier)
			print("Attacker Controller created!!!!")
		else:
			print("----Creating Defender Controller----")
			servant = RobotControllerDefenderI(robot, identifier)
			print("Defender Controller created!!!!")

		robotprx = current.adapter.addWithUUID(servant)
		current.adapter.createDirectProxy(robotprx.ice_getIdentity())
		robot_prx = drobots.RobotControllerFactoryPrx.uncheckedCast(robotprx)
		print(robot_prx)

		return robot_prx


class RobotControllerDefenderI(drobots.RobotController):
	def __init__(self, robot, identificator):
		self.robot = robot
		self.identificator = identificator

	def turn(self, current=None):
		print("----Defensor Turn {}----".format(self.identificator))

	def robotDestroyed(self, current=None):
		print("----Robot destroyed: {}----".format(self.identificator))

	def location():
		print("----{} location has been sent----".format(self.identificator))

	def scan():
		print("----The robot {} has scanned----".format(self.identificator))


class RobotControllerAttackerI(drobots.RobotController):
	def __init__(self, robot, identificator):
		self.robot = robot
		self.identificator = identificator

	def turn(self, current=None):
		print("----Attacker Turn {}----".format(self.identificator))

	def robotDestroyed(self, current=None):
		print("----Robot destroyed: {}----".format(self.identificator))

	def location():
		print("----{} location has been sent----".format(self.identificator))

	def scan():
		print("----The robot {} has scanned----".format(self.identificator))


class Client(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		adapter = broker.createObjectAdapter("FactoryAdapter")
		adapter.activate()

		factory_servant = RobotControllerFactoryI()
		factory_prx = adapter.add(factory_servant, broker.stringToIdentity("factory"))
		print(factory_prx)

		sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sckt.connect(("google.es", 80))
		ip = sckt.getsockname()[0]
		sckt.close()

		factory_container_prx = broker.stringToProxy("container -t -e 1.1:tcp -h {} -p 6060 -t 60000".format(ip))
		factory_container = Services.ContainerPrx.checkedCast(factory_container_prx)

		if factory_container == None:
			raise Ice.NoEndpointException()
		else:
			factory_identifier = len(factory_container.list())
			factory_container.link(str(factory_identifier), factory_prx)

		sys.stdout.flush()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

client = Client()
sys.exit(client.main(sys.argv))
