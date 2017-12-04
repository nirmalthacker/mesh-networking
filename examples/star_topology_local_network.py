from time import sleep

from mesh.links import VirtualLink
from mesh.programs import Switch, Printer
from mesh.node import Node


'''
Simple Star Topology Example:
         n1
         |
       (star)
        /  \
      n2    n3

Star Node is a switch that forwards all packets to all its links
Each Node is a printer that Prints its packets
'''

ls = (VirtualLink('vl1'), VirtualLink('vl2'), VirtualLink('vl3'))

nodes = (
    Node([ls[0], ls[1], ls[2]], 'star', Program=Switch),
    Node([ls[0]], 'n1', Program=Printer),
    Node([ls[1]], 'n2', Program=Printer),
    Node([ls[2]], 'n3', Program=Printer)
)

[l.start() for l in ls]
[n.start() for n in nodes]


if __name__ == "__main__":
    print('\n', nodes)
    print("Experiment by typing packets for [n1] to send out, and seeing if they make it to the [n2], [n3]")

    try:
        while True:
            print("------------------------------")
            message = input("[n0]  OUT:")
            nodes[1].send(bytes(message, 'UTF-8'))
            sleep(1)

    except (EOFError, KeyboardInterrupt):   # CTRL-D, CTRL-C
        print(("All" if all([n.stop() for n in nodes]) else 'Not all') + " nodes stopped cleanly.")
        print(("All" if all([l.stop() for l in ls]) else 'Not all') + " links stopped cleanly.")
