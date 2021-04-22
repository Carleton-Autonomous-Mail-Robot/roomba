# @author: Devon Daley

from reader import *

# This is where the path is constructed so that the robot knows which nodes to follow

'''		nodeDistances FORMAT
(Node1: Node2 Node2Hops Node3 Node3Hops Node4 Node4Hops)
(Node2: Node1 Node1Hops Node3 Node3Hops Node4 Node4Hops)
(Node3: Node1 Node1Hops Node2 Node2Hops Node4 Node4Hops)
(Node4: Node1 Node1Hops Node2 Node2Hops Node3 Node3Hops)

		nodeTraversal FORMAT
(Node1Node2: Node2Node3 Angle23 Node3Node4 Angle34)
(Node2Node3: Node1Node2 Angle12 Node3Node4 Angle34)
(Node3Node4: )

'''


class PathFinder():

	def __init__(self):
		# Get all navigation information
		self.reader = NodeReader()
		self.dist = self.reader.read_distances()
		self.trav = self.reader.read_traversal()
    
	'''
		A utility to find the best path given a source and destination node
	'''
	def find_path(self,src,dst):
		
        # Construct path of nodes without angles
        # <----------------------------------------------------------------------------REPLACE SECTION WITH PROPER A STAR ALGORITHM
		distance = int(self.dist[src][dst])		# Distance from destination
		path = src + ' '
		while not distance == 0:
			path = path + self.next_step(path[-2],dst) + ' '
			distance = distance - 1
        
        # Calculate necessary angles between node vectors (eg Node1Node2). Construct new dict to store path with angles to turn in between
		split = path.split()
		newpath = []
		newpath.append(split[0])
		newpath.append(180)
		sindex = 1		# for accessing split
		index = 2		# for accessing newpath
		while index < len(split) + 1:
			newpath.append(split[sindex])
			str1 = ''
			region1 = str1.join(sorted((newpath[index - 2],newpath[index])))
			str1 = ''
			try:
				region2 = str1.join(sorted((split[sindex+1],newpath[index])))
			except IndexError:
				return newpath
			newpath.append(self.trav[region1][region2])	# Get the angle between regions
			index = index + 2
			sindex = sindex + 1
		newpath.append(split[sindex])
			
		return newpath
		
	# Given current node and dst node, what is next step? Returns a Letter to represent node
	def next_step(self, curr, dst):
		adjacent = dict()
		# Find adjacent nodes
		for c in self.dist[curr]:
			if self.dist[curr][c] == 1:
				if c == dst:		# last entry
					return dst
				else:
					adjacent[c] = self.dist[c][dst]	# adjacent[c[0]] = distance from dest
		
		# Find nodes closer to dest than curr
		nextnode = ''
		for node in adjacent:
			if self.dist[curr][dst] > self.dist[node][dst]:
				nextnode = node[0]
				break
				
		return nextnode
