from visual import *
from cell import *
from cellHelper import *
import sys
import math


# filename = "cluster_for_figure_2.csv"

# network_elements = constructNetworkFromDataFile(filename)

# # for cellular_gui in network_elements:
# # 	# lunchbox = box(pos=cellular_gui.pos, color=color.green, length = cellular_gui.diameter, height=cellular_gui.diameter, width = cellular_gui.diameter)
# # 	print cellular_gui.pos, cellular_gui.axis
# # 	cellular_gui.graphical.color = color.green
# # 	scene.kb.getkey()
# # 	cellular_gui.graphical.color = color.orange
# # 	# lunchbox.visible = False

# # output_cell_data_file(network_elements, "cluster_for_figure_2.csv")

# scene.kb.getkey()

# child = network_elements[5]

# # child.graphical.color = color.blue

# parent = network_elements[1]

# rotate_about = parent.axis

# rotated_pos = rotateVec(child.pos, rotate_about, math.pi)

# rotated_axis = rotateVec(child.axis, rotate_about, math.pi)

# print rotated_pos

# child.pos = rotated_pos

# child.graphical.pos = rotated_pos

# child.axis = rotated_axis

# child.graphical.axis = rotated_axis

# output_cell_data_file(network_elements, "franken_network.csv")

# clearScene(scene)

# network_elements = []

network_elements = constructNetworkFromDataFile("franken_network.csv")

# for element in network_elements:
# 	orig_color = element.graphical.color
# 	element.graphical.color = color.blue
# 	scene.kb.getkey()
# 	element.graphical.color = orig_color

key = scene.kb.getkey()

while key != 'a':

	next_victim = network_elements[4]
	parent = network_elements[0]
	old_length = next_victim.length
	rotate_about = parent.axis
	original_pos = next_victim.pos
	original_axis = next_victim.axis
	angle_in_rads = 0.0872665
	if key == 'f':
		rotated_pos = rotateVec(original_pos, rotate_about, angle_in_rads)
		rotated_axis = rotateVec(original_axis, rotate_about, angle_in_rads)
	elif key == 'b':
		rotated_pos = rotateVec(original_pos, rotate_about, -angle_in_rads)
		rotated_axis = rotateVec(original_axis, rotate_about, -angle_in_rads)

	next_victim.axis = rotated_axis
	next_victim.graphical.axis = rotated_axis
	
	next_victim.pos = rotated_pos
	next_victim.graphical.pos = rotated_pos

	next_victim.length = old_length
	next_victim.graphical.length = old_length
	key = scene.kb.getkey()



key = scene.kb.getkey()


while key != 'a':

	next_victim = network_elements[6]
	next_victim_two = network_elements[2]
	parent = network_elements[0]

	old_length = next_victim.length
	old_length_two = next_victim_two.length

	rotate_about = parent.axis
	original_pos = next_victim.pos
	original_axis = next_victim.axis

	original_pos_two = next_victim_two.pos
	original_axis_two = next_victim_two.axis

	angle_in_rads = 0.0872665
	if key == 'f':
		rotated_pos = rotateVec(original_pos, rotate_about, angle_in_rads)
		rotated_axis = rotateVec(original_axis, rotate_about, angle_in_rads)
		rotated_pos_two = rotateVec(original_pos_two, rotate_about, angle_in_rads)
		rotated_axis_two = rotateVec(original_axis_two, rotate_about, angle_in_rads)
	elif key == 'b':
		rotated_pos = rotateVec(original_pos, rotate_about, -angle_in_rads)
		rotated_axis = rotateVec(original_axis, rotate_about, -angle_in_rads)
		rotated_pos_two = rotateVec(original_pos_two, rotate_about, -angle_in_rads)
		rotated_axis_two = rotateVec(original_axis_two, rotate_about, -angle_in_rads)

	next_victim.axis = rotated_axis
	next_victim.graphical.axis = rotated_axis
	next_victim_two.axis = rotated_axis_two
	next_victim_two.graphical.axis = rotated_axis_two
	
	next_victim.pos = rotated_pos
	next_victim.graphical.pos = rotated_pos
	next_victim_two.pos = rotated_pos_two
	next_victim_two.graphical.pos = rotated_pos_two

	next_victim.length = old_length
	next_victim.graphical.length = old_length
	next_victim_two.length = old_length_two
	next_victim_two.graphical.length = old_length_two

	key = scene.kb.getkey()


output_cell_data_file(network_elements, "fixed_figure_network.csv")

network_elements = []

clearScene(scene)

network_elements = constructNetworkFromDataFile("fixed_figure_network.csv")

for element in network_elements:
	element.graphical.color = color.blue

scene.kb.getkey()

sys.exit(0)