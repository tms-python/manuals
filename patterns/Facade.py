class VirtualMachine:

    def create_network(self):
        print('Network has been created')

    def create_volume(self):
        print('Volume has been created')

    def get_ip(self):
        print('Got ip 195.50.4.15')

    def attach_ip(self):
        print('IP address has been attached to VM')

    def release_network(self):
        print('Network released')

    def release_volume(self):
        print('Volume released')

    def release_ip(self):
        print('ip 195.50.4.15 released')

    def detach_ip(self):
        print('IP address detached')


class VirtualMachineFacade:
    __vm = None

    def __init__(self):
        self.__vm = VirtualMachine()

    def create_vm(self):
        self.__vm.create_network()
        self.__vm.create_volume()
        self.__vm.get_ip()
        self.__vm.attach_ip()

    def delete_vm(self):
        self.__vm.detach_ip()
        self.__vm.release_ip()
        self.__vm.release_volume()
        self.__vm.release_network()


vm = VirtualMachineFacade()
vm.create_vm()
print()
vm.delete_vm()