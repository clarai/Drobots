import Ice
import Services

class ContainerI(Services.Container):

    def __init__(self):
        self.proxies = {}
        self.attackers = {}
        self.defenders = {}

    def link(self, key, proxy):
        if (key in self.proxies) or (key in self.attackers) or (key in self.defenders):
            raise Services.AlreadyExists(key)
        else:
            if 'factory_rc' in key:
                self.proxies[key] = proxy
            elif 'attackers_rc' in key:
                self.attackers[key] = proxy
            elif 'defenders_rc' in key:
                self.defenders[key] = proxy
        print("The created link is: {0} -> {1}".format(key, proxy))

    def unlink(self, key):
        if (key not in self.proxies) or (key not in self.attackers) or (key not in self.defenders):
            raise Services.NotSuchKey(key)
        else:
            if 'factory_rc' in key:
                del self.proxies[key]
            elif 'attackers_rc' in key:
                del self.attackers[key]
            elif 'defenders_rc' in key:
                del self.defenders[key]
        print("The deleted link is: {0}".format(key))

    def list(self, dic, pid):
        if dic == 0:
            return self.proxies
        elif dic == 1:
            self.d = {}
            for i in self.attackers.keys():
                if str(pid) in i:
                    self.d[i] = attackers[x]
            return self.d
        elif dic == 2:
            self.d = {}
            for i in self.defenders.keys():
                if str(pid) in i:
                    self.d[i] = defenders[x]
            return self.d

class Server(Ice.Application):
    def run(self,argv):
        broker = self.communicator()
        servant = ContainerI()

        adapter = broker.createObjectAdapter("containerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentify("container"))
        print(proxy)

        sys.stdout.flush()

        adapter.activate()
        
        self.shutDownOnnterrupt()
        broker.waitforShutdown()

        return 0

if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
