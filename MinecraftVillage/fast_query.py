# This module is based on mcpi_fast_query by joseph-reynolds
# https://github.com/joseph-reynolds/mcpi_fast_query
#
# Some changes were made to get it working with Python 3,
# and functions added to query the surface of the world, rather
# than 3D volumes of blocks or a flat surface.
#
# B. Grayland/s3927837/marmaladian

# from __future__ import absolute_import, division, print_function

import mcpi.minecraft as minecraft
import mcpi.block as block
from   mcpi.vec3 import Vec3
from   mcpi.connection import Connection
import collections
import io
import select
import socket
import threading
import time
import timeit
import queue

global mc

class Cuboid:
	"""A cuboid represents a 3-dimensional rectangular area

	The constructor takes ranges along the x, y, and z axis,
	where each range is a tuple(min, max) of world coordinates.
	Ranges are integers and are used like the Python built-in range
	function where the second number is one past the end.  Specifically,
	to get a single point along an axis, use something like tuple(0, 1).

	Examples:
	  # A point at (100,12, 5)
	  >>> point = Cuboid((100,101), (12,13), (5,6))
	  
	  # An 11 by 11 square centered around (0,0):
	  >>> c = Cuboid((-5, 6), (0, 1), (-5, 6))
	  >>> c.x_range
	  (-5, 6)
	  >>> g = c.generate()
	  >>> for point in g: print(p)
	"""
	def __init__(self, x_range, y_range, z_range):
		if x_range[0] >= x_range[1]: raise RuntimeError("bad x")
		if y_range[0] >= y_range[1]: raise RuntimeError("bad y")
		if z_range[0] >= z_range[1]: raise RuntimeError("bad z")
		self.x_range = x_range
		self.y_range = y_range
		self.z_range = z_range
	
	def __repr__(self):
		return "(%s, %s, %s)" % (str(self.x_range), str(self.y_range), str(self.z_range))
	
	def generate(self):
		for x in range(*self.x_range):
			for y in range(*self.y_range):
				for z in range(*self.z_range):
					yield (x, y, z)

	def generate_xz(self):
		for x in range(*self.x_range):
			for z in range(*self.z_range):
				yield (x, z)

	def total_blocks(self):
		return ((self.x_range[1] - self.x_range[0]) *
				(self.y_range[1] - self.y_range[0]) *
				(self.z_range[1] - self.z_range[0]))

### --------------------------------------------------------------------
### Query the Minecraft server from multiple threads AND stuffing
### multiple requests into the socket before getting a reply.
### --------------------------------------------------------------------
"""query_blocks

Purpose:
  This generator is for getting a lot of data from the Minecraft server
  quickly.  For example, if you want data from a thousand blocks you
  could call getBlock for each block, but that would take a long time.
  This function essentially calls getBlock for many blocks at the same
  time, thus improving throughput.
  If you want data for just a few blocks, prefer to use getBlock.

  The following query functions are supported:
	world.getBlock(x,y,z) -> blockId
	world.getBlockWithData(x,y,z) -> blockId,blockData
	world.getHeight(x,z) -> y

  Parameters:
	requests
			An iterable of coordinate tuples.  See the examples.
			Note that this will be called from different threads.
	fmt
			The request format string, one of:
				world.getBlock(%d,%d,%d)
				world.getBlockWithData(%d,%d,%d)
				world.getHeight(%d,%d)
	parse_fn
			Function to parse the results from the server, one of:
				int
				tuple(map(int, ans.split(",")))
	thread_count
			Number of threads to create.

  Generated values:
	tuple(request, answer), where
	  request - is a value from the "requests" input parameter
	  answer - is the response from the server, parsed by parse_fn    

Query the Minecraft server quickly using two techniques:
 1. Create worker threads, each with its own socket connection.
 2. Each thread sends requests into the socket without waiting
	for responses.  Responses are then matched with requests.

The low-level design notes:
 - This uses a straightforward thread model
 - Creating more than 50 threads gets expensive.
 
 - The main thread creates the following
	 request_lock = threading.Lock()  # Serialize access to requests
	 answer_queue = queueing.Queue()  # Get answers from threads
	 threads = threading.Thread()     # Worker threads
 - each thread:
	 more_requests = True
	 pending_request_queue = deque()
	 loop until more_requests==False and pending_request_queue is empty:
	   if more_requests:
		 with request_lock:
			try:
				request = request_iter.next()
			except StopIteration:
				more_requests = False
				continue
			request_buffer = request_buffer + (fmt % request) + "\n"
			pending_request_queue.append(request)
		 etc...

Constraints:
 - the "requests" iterator is invoked serially from different threads,
   so lists and simple generators work okay, but fancy stuff may not.
 - the order in which answers come back is not deterministic
"""

def query_blocks(requests, fmt, parse_fn, thread_count = 20):
	def worker_fn(mc_socket, request_iter, request_lock, answer_queue,):
		more_requests = True
		request_buffer = bytes()
		response_buffer = bytes()
		pending_request_queue = collections.deque()
		while more_requests or len(pending_request_queue) > 0:
			# Grab more requests
			while more_requests and len(request_buffer) < 4096:
				with request_lock:
					try:
						request = next(request_iter)
					except StopIteration:
						more_requests = False
						continue
					new_request_str = (fmt % request) + "\n"
					request_buffer = request_buffer + new_request_str.encode('utf-8')
					# request_buffer = request_buffer + (fmt % request) + "\n"
					pending_request_queue.append(request)

			# Select I/0 we can perform without blocking
			w = [mc_socket] if len(request_buffer) > 0 else []
			r, w, x = select.select([mc_socket], w, [], 5)
			allow_read = bool(r)
			allow_write = bool(w)

			# Write requests to the server
			if allow_write:
				# Write exactly once
				bytes_written = mc_socket.send(request_buffer)
				request_buffer = request_buffer[bytes_written:]
				if bytes_written == 0:
					raise RuntimeError("unexpected socket.send()=0")

			# Read responses from the server
			if allow_read:
				# Read exactly once
				bytes_read = mc_socket.recv(1024)
				response_buffer = response_buffer + bytes_read
				if bytes_read == 0:
					raise RuntimeError("unexpected socket.recv()=0")

			# Parse the response strings
			responses = response_buffer.split('\n'.encode('utf-8'))
			response_buffer = responses[-1]
			responses = responses[:-1]
			for response_string in responses:
				request = pending_request_queue.popleft()
				answer_queue.put((request, parse_fn(response_string)))

	request_lock = threading.Lock() # to serialize workers getting
									# the next request
	answer_queue = queue.Queue()  # To store answers coming back from
								  # the worker threads
	sockets = []
	try:
		for i in range(thread_count):
			sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
			sockets[-1].connect(("localhost", 4711))
		workers = []
		threading.stack_size(128 * 1024)  # bytes
		for w in range(thread_count):
			t = threading.Thread(target = worker_fn,
								 args = (sockets[w],
										 iter(requests),
										 request_lock,
										 answer_queue))
			t.start()
			workers.append(t)
			
		# Wait for workers to finish
		for w in workers:
			w.join()
	except socket.error as e:
		print("Socket error:", e)
		print("Is the Minecraft server running?")
		raise e
	finally:
		for s in sockets:
			try:
				s.shutdown(socket.SHUT_RDWR)
				s.close()
			except socket.error as e:
				pass
	
	# Collect results
	while not answer_queue.empty():
		yield answer_queue.get()


def fq_heights(query_cuboid):
	"""
	Parameter query_cuboid is a Cuboid representing the area you want to
	get heights for. The y component is ignored.
	
	The function returns a dictionary mapping (x, z) to (height).
	"""
	region = Cuboid(query_cuboid.x_range, (0,1), query_cuboid.z_range)
	result = {}

	for pos, h in query_blocks(
			region.generate_xz(),
			"world.getHeight(%d,%d)",
			int):
		result[pos] = h
	
	return result

def _heightmap_to_surface(heightmap):
	for xz, y in heightmap.items():
		yield (xz[0], y, xz[1])

def fq_heights_and_surface_ids(query_cuboid):
	"""
	Parameter query_cuboid is a Cuboid representing the area you want to
	get heights for. The y component is ignored.
	
	The function returns a dictionary mapping (x, z) to (height, block_id)
	where the block_id is the block at the surface.
	"""
	
	heightmap = fq_heights(query_cuboid)
	surface_coords = _heightmap_to_surface(heightmap)
	
	result = {}

	for pos, blk in query_blocks(
			surface_coords,
			"world.getBlock(%d,%d,%d)",
			int):
		result[(pos[0], pos[2])] = (pos[1], blk)

	return result

def fq_draw_heights(hmap, x_range, z_range, detailed=False):
	"""
	Renders an ASCII image of the heightmap for debugging purposes.
	"""
	min_height = hmap[min(hmap, key=hmap.get)]
	max_height = hmap[max(hmap, key=hmap.get)]
	height_range = max_height - min_height

	GRADIENT = ' .:-=+*#%@'
	if detailed:
		GRADIENT = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!lI;:,"^`. '[::-1]
		
	scaling = len(GRADIENT)/height_range

	for z in range(*z_range):
		s = ""
		for x in range(*x_range):
			y = hmap[x,z]
			c = '{:2}'.format(GRADIENT[int((y - min_height - 1) * scaling)])
			s = s + c
		print(s)


if __name__ == "__main__":
	# this is for testing/timing
	try:
		mc = minecraft.Minecraft.create()
	except socket.error as e:
		print("Cannot connect to Minecraft server")
		raise e

	px, py, pz = mc.player.getTilePos()

	test_cuboid = Cuboid((px-20,px+21), (py-20, py+21), (pz-20, pz+21))

	# Start the timer
	starttime = timeit.default_timer()

	height_map = fq_heights(test_cuboid)
	block_map = fq_heights_and_surface_ids(test_cuboid)
		
	# Stop the timer
	endtime = timeit.default_timer()
	total_block_count = test_cuboid.total_blocks()
	overall_time = endtime - starttime

	# Announce results
	print("Total", total_block_count, "blocks in",
		  overall_time, 'seconds')
	print("Overall:", total_block_count / overall_time,
		  "blocks/second")

	fq_draw_heights(height_map, test_cuboid.x_range, test_cuboid.z_range, detailed=False)