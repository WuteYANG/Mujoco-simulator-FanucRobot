import math
import time
import os
import numpy as np
from mujoco_py import load_model_from_xml, MjSim, MjViewer
import Lrmate_functions as lrc

MODEL_XML = """
<?xml version="1.0" encoding="utf-8"?>
<mujoco>
    <compiler angle="radian" coordinate="local"/>
    <default>
        <geom friction="0.8 0.8 0.8" conaffinity="1" condim="1" contype="1" margin="0.0005"/>
    </default>
    <actuator>
	<position ctrllimited="true" ctrlrange="-3.1416 3.1416" joint="link1" kp="100" name="link1"/>
	<position ctrllimited="true" ctrlrange="-3.1416 3.1416" joint="link2" kp="100" name="link2"/>
	<position ctrllimited="true" ctrlrange="-3.1416 3.1416" joint="link3" kp="100" name="link3"/>
	<position ctrllimited="true" ctrlrange="-3.1416 3.1416" joint="link4" kp="100" name="link4"/>
	<position ctrllimited="true" ctrlrange="-3.1416 3.1416" joint="link5" kp="100" name="link5"/>
	<position ctrllimited="true" ctrlrange="-3.1416 3.1416" joint="link6" kp="100" name="link6"/>
    </actuator>
    <sensor>
	<jointpos name="s_j1" joint="link1"/>
	<jointpos name="s_j2" joint="link2"/>
	<jointpos name="s_j3" joint="link3"/>
	<jointpos name="s_j4" joint="link4"/>
	<jointpos name="s_j5" joint="link5"/>
	<jointpos name="s_j6" joint="link6"/>
    </sensor>
    <asset>
        <mesh file="Base.STL" name="base" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Link1.STL" name="link1" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Link2.STL" name="link2" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Link3.STL" name="link3" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Link4.STL" name="link4" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Link5.STL" name="link5" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Link6.STL" name="link6" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Sensor.STL" name="sensor" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Palm.STL" name="palm" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Finger1.STL" name="finger1" scale="0.001 0.001 0.001"></mesh>
	<mesh file="Finger2.STL" name="finger2" scale="0.001 0.001 0.001"></mesh>
    </asset>
    <worldbody>
        <body name="base">
	    <inertial diaginertia="0 0 0" mass="0" pos="0 0 0" quat="0 0 0 0"/>
            <geom type="mesh" mesh="base" name="base" pos="0 0 0.33" rgba="0.5 0.5 0.5 1"></geom>
	    <body name="link1">
	        <inertial diaginertia="0.0233 0.0194 0.0139" mass="2.3984" pos="0.0186 0.0034 -0.0771" quat="0.7071 -0.7071 0 0"></inertial>
		<joint axis="0 0 1" damping="1000" name="link1" range="-3.1416 3.1416" type="hinge"/>
                <geom type="mesh" mesh="link1" name="link1" pos="0.05 0.0 0.33" quat="0.7071 -0.7071 0 0" rgba="1 1 0 1"></geom>
		<body name="link2">
	            <inertial diaginertia="0.0329 0.2070 0.1884" mass="7.8019" pos="-0.0071 -0.1326 0.0248" quat="0 0.7071 -0.7071 0"></inertial>
		    <joint axis="0 1 0" pos="0.05 0.0 0.33" damping="1000" name="link2" range="-3.1416 3.1416" type="hinge"/>
		    <geom type="mesh" mesh="link2" name="link2" pos="0.05 0.0 0.77" euler="1.57 0 1.57" rgba="1 1 0 1"></geom>
		    <body name="link3">
		        <inertial diaginertia="0.0081 0.0069 0.0080" mass="2.9847" pos="0.0058 -0.0059 -0.0207" quat="0 0.7071 -0.7071 0"></inertial>
			<joint axis="0 -1 0" pos="0.05 0.0 0.77" damping="1000" name="link3" range="-3.1416 3.1416" type="hinge"/>
		        <geom type="mesh" mesh="link3" name="link3" pos="0.05 0.0 0.805" euler="1.57 -1.57 1.57" rgba="1 1 0 1"></geom>
			<body name="link4">
		            <inertial diaginertia="0.0529 0.0057 0.0532" mass="4.1442" pos="-0.0002 0.0028 -0.2061" quat="0.7071 0.7071 0 0"></inertial>
			    <joint axis="-1 0 0" pos="0.47 0.0 0.805" damping="1000" name="link4" range="-3.1416 3.1416" type="hinge"/>
		            <geom type="mesh" mesh="link4" name="link4" pos="0.47 0.0 0.805" euler="1.57 0 1.57" rgba="1 1 0 1"></geom>
			    <body name="link5">
		                <inertial diaginertia="0.0025 0.0024 0.0012" mass="1.7004" pos="0.0000 -0.0274 -0.0044" quat="0.7071 -0.7071 0 0"></inertial>
				<joint axis="0 -1 0" pos="0.47 0.0 0.805" damping="1000" name="link5" range="-3.1416 3.1416" type="hinge"/>
		                <geom type="mesh" mesh="link5" name="link5" pos="0.47 0.0 0.805" euler="1.57 -1.57 1.57" rgba="1 1 0 1"></geom>
				<body name="link6">
		                    <inertial diaginertia="0.00003 0.00003 0.00005" mass="1.1700" pos="0.0 0.0 -0.08" quat="0 1 0 0"></inertial>
				    <joint axis="1 0 0" pos="0.55 0.0 0.805" name="link6" range="-3.1416 3.1416" type="hinge"/>
		                    <geom type="mesh" mesh="link6" name="link6" pos="0.55 0.0 0.805" euler="1.57 1.57 1.57" rgba="0 0 0 1"></geom>
				    <body name="sensor">
            				<geom type="mesh" mesh="sensor" name="sensor" pos="0.62 -0.0325 0.7725" euler="0 -1.57 0" rgba="0.7 0.7 0.7 1"></geom>
					<body name="palm">
            				    <geom type="mesh" mesh="palm" name="palm" pos="0.703 -0.07 0.7875" euler="0 0 1.57" rgba="0.7 0.7 0.7 1"></geom>
					    <body name="finger1">
            				        <geom type="mesh" mesh="finger1" name="finger1" pos="0.700 -0.027 0.7875" euler="1.57 0 0" rgba="0.7 0.7 0.7 1"></geom>
				            </body>
					    <body name="finger2">
            				        <geom type="mesh" mesh="finger2" name="finger2" pos="0.700 0.027 0.7875" euler="1.57 0 0" rgba="0.7 0.7 0.7 1"></geom>
				            </body>
				        </body>
				    </body>
				</body>6
			    </body>
			</body>
		    </body>
                </body>
            </body>
        </body>    
	<body name="floor" pos="0 0 -0.02">
            <geom size="0.2 0.2 0.02" density="0" rgba="0 1 0 1" type="box"/>
        </body>
    </worldbody>
</mujoco>
"""

# Initialize Mujoco
model = load_model_from_xml(MODEL_XML)
sim = MjSim(model)
viewer = MjViewer(sim)
step = 0
i = 0
pi = 3.141592654
r2d = 180/pi




# Main loop
while True:
    
    # set joint position
    lrc.control_robot(sim)

    # Update robot state
    state = lrc.robot_info_update(sim)

    # print joint position
    if step%50 == 0:
        #state = sim.get_state()
        #print("Joint Positions(deg):", state.qpos*r2d)
        print(state)

	
    # Viewer angle
    lrc.viewer(viewer)

    if step <= 200:
        step += 1
    if step > 200 and os.getenv('TESTING') is not None:
        break
