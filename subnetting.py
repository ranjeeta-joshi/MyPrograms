"""
Module to compute number of hosts per subnetwork and
number of subnetworks from given ipaddress and prefix length
"""

import sys
import re


class Subnet(object):
    """
    This program outputs following for a given ipaddress with prefix length
    1. Number of hosts per subnet,
    2. Number of subnetworks,
    3. Is the address classful,
    4. Which class the ipaddress falls under,
    5. Network ID of given ipaddress,
    6. Broadcast ID of given ipaddress.
    """

    def __init__(self, ipaddr):
        """
        To initialize Ipaddress with prefix length

        Attributes:
            :param ipaddr (str): Ipaddress with prefix length -
                                 Example: 192.168.1.1/24

        Raises:
            Index Error: if ipaddr doesn't contain prefix length
                         when the string split.

            Value Error: if prefix length is less than 8 or greater than 30
        """
        try:
            self.ipaddr = ipaddr.split("/")[0]
            self.prefix = int(ipaddr.split("/")[1])
            if 8 <= self.prefix <= 30:
                pass
            else:
                raise ValueError
        except IndexError:
            print "Please pass valid ipaddress with prefix " \
                  "length, example: 192.168.1.1/24"
            sys.exit(1)
        except ValueError:
            print "Please pass valid prefix length between 8 to 30"
            sys.exit(1)

    @staticmethod
    def cidr2bin(prefix):
        """
        :Static method: Converts prefix length to binary equivalent

        :param prefix (int): Prefix length to be converted into
                             binary equivalent.

        :return (str): Binary form of prefix length
        """
        return "1" * prefix + "0" * (32-prefix)

    def get_subnetmask(self):
        """
        This Method convert CIDR notation of subnet mask to
        dot decimal notation of subnet mask
        i.e., /24 to 255.255.255.0

        :return (str): Subnet mask in dotted decimal format.
        """
        subnet = [str(int(x, 2))
                  for x in re.findall
                  ('.{1,8}', self.cidr2bin(self.prefix))]
        return ".".join(subnet)

    def get_ipaddr(self):
        """
        Method to get the ipaddress only without prefix length.

        :return (str): Ipaddress in dotted decimal.
        """
        return self.ipaddr

    def get_hosts_per_subnet(self):
        """
        Method to calculate number of hosts per subnet for
        a given ipaddress with prefix length.

        :return (int): Number of hosts per subnet.
        """
        nhosts = 2**(32-self.prefix) - 2
        return nhosts

    def get_subnetworks(self):
        """
        Method to calculate number of subnetworks for a given
        ipaddress with prefix length.

        :return (int): Number of subnetworks.
        """
        return 2**self.prefix

    def is_classful(self):
        """
        Method to check whether given ipaddress with prefix length
        is a classful ipaddres. i.e., Class A,B and C

        :return (Bool): True if given ipaddress is classful else False
        """
        if self.network_class() == "Classless":
            return False
        else:
            return True

    def network_class(self):
        """
        Method to check the given ipaddress belongs to which class
        if it is a classful address.

        :return (str): Class A, B, C else Classless
        """
        ipbyte = int(self.ipaddr.split(".")[0])
        if 0 <= ipbyte <= 127 and self.prefix == 8:
            return "Class A"
        elif 128 <= ipbyte <= 191 and self.prefix == 16:
            return "Class B"
        elif 192 <= ipbyte <= 223 and self.prefix == 24:
            return "Class C"
        else:
            return "Classless"

    def get_netid(self):
        """
        Method to find Network id for a given Ipaddress.

        :return (str): Network ipaddress in dotted decimal format.
        """
        iplist = list(map(int, self.ipaddr.split(".")))
        subnetlist = list(map(int, self.get_subnetmask().split(".")))
        return ".".join([str(a & b) for a, b in zip(iplist, subnetlist)])

    def get_broadcastid(self):
        """
        Method to find Broadcast id for a given Ipaddress.

        :return (str): Broadcast ipaddress in dotted decimal format.
        """
        iplist = list(map(int, self.get_netid().split(".")))
        subnetlist = list(map(int, self.get_subnetmask().split(".")))
        return ".".join([str(256 + (~(a ^ b)))
                         for a, b in zip(iplist, subnetlist)])


if __name__ == '__main__':
    inett = Subnet("192.168.1.1/23")
    print inett.get_subnetmask()
    print inett.get_hosts_per_subnet()
    print inett.get_subnetworks()
    print inett.get_netid()
    print inett.get_broadcastid()
    print inett.network_class()
    print inett.is_classful()






