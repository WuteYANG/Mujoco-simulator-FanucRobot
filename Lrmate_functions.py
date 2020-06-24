import math
import time
import os
import numpy as np
from mujoco_py import load_model_from_xml, MjSim, MjViewer


def initial_mujoco(MODEL_XML):
    # Initialization
    model = load_model_from_xml(MODEL_XML)
    sim = MjSim(model)
    viewer = MjViewer(sim)


def robot_info_update(sim):
    state = sim.get_state()
    return state

def control_robot(sim):
    sim.data.set_joint_qpos('link1', 0.)
    sim.data.set_joint_qpos('link2', 0.)
    sim.data.set_joint_qpos('link3', 0.)
    sim.data.set_joint_qpos('link4', 0.)
    sim.data.set_joint_qpos('link5', -np.pi/2)
    sim.data.set_joint_qpos('link6', 0.)
    sim.forward()

def viewer(viewer):
    # Viewer angle
    viewer.cam.distance = 2 # viewer distance
    viewer.cam.azimuth = 215. # viewer angle (deg)
    viewer.cam.elevation = -6.
    viewer.render()
    

	


    
    
    

