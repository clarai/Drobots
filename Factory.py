import Ice

class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")

        factory_servant = RobotControllerFactoryI()

        container_prx = broker.stringToProxy("container -t -e 1.1 @ Container.containerAdapter")

        container = Services.ContainerPrx.checkedCast(container_prx)

        if container == None:
            raise Ice.NoEndpointException()
        else:
            print("Success in connecting to the container")

        proxy = adapter.add(factory_servant, broker.stringToIdentify("factory"))
        print(proxy)

        sys.stdout.flush()

        adapter.activate()

        self.shutDownOnnterrupt()
        broker.waitforShutdown()

        return 0

if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))

class RobotControllerFactoryI(factory.RobotControllerFactory):
    def make(self, robot_prx, pid):
        if(robot_prx.ice_IsA("::drobots::Attacker")):
            print("Creating Attacker Controller")
            servant = RobotControllerAttackerI(robot_prx, pid)
            print("Attacker Controller created")
        else:
            print("Creating Defender Controller")
            servant = RobotControllerDefenderI(robot_prx, pid)
            print("Defender Controller created")
        proxy = current.adapter.addWithUUID(servant)
        current.adapter.createDirectProxy(proxy.ice_getIdentity())

        return 0 #SE PONE ESO PORQUE NO TENEMOS NI IDEA :D

class RobotControllerAttackerI(factory.RobotControllerAttacker):
    def __init__(self, robot, pid):
        self.robot = robot
        self.pid = pid


    def location(self, coordinates):
    def objective(self, coordinates):



class RobotControllerDefenderI(factory.RobotControllerDefender):
    def location(self, coordinates):


