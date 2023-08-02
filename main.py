from node import Node
from multiprocessing import Process

if __name__ == "__main__":
    nodes = [5000, 5001, 5002]  # list of nodes in the system, by port number
    processes = []

    for id, port in enumerate(nodes):
        node = Node(id, port, nodes)
        p = Process(target=node.run)
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()