#!/usr/bin/env python3

# this code is developed to tune BC parameters to match target in the output using SimVascular 1D solver 

import os
from pathlib import Path
import sv
import sys
import vtk

# A: ================================================ CODE INPUTS ============================================

# A1: python script directory
script_dir = '/Desktop/SimVascular/GeneralizedCoAmodel/PyInterface/Example01'

# A2: input files directory
input_dir = os.path.join(script_dir,'input')
print(input_dir)

# A3: output file directory
output_dir = os.path.join(script_dir,'output')
print(output_dir)

# A4: inlet/outlet face names
inlet_face_name_AA            = 'cap_S01_AA'
outlet_face_name_RS           = 'cap_S02_RS'
outlet_face_name_RC           = 'cap_S03_RC'
outlet_face_name_LC           = 'cap_S04_LC'
outlet_face_name_LS           = 'cap_S05_LS'
outlet_face_name_DA           = 'cap_S01_AA'

# A5: other names
mdlname                       = "Control"
flowwf_file_name              = 'inflow.flow' 

# B: ========================================== CREATE ROM SIMULATION =========================================
rom_simulation = sv.simulation.ROM() 

# C: ===================================== CREATE ROM SIMULATION PARAMETERS ===================================
params = sv.simulation.ROMParameters()

# D: ============================================= MESH PROPERTIES ===========================================
mesh_params = params.MeshParameters()

# E ======================================== CREATE MODEL PARAMETERS =========================================
model_params = params.ModelParameters()
model_params.name = mdlname
model_params.inlet_face_names = [inlet_face_name_AA ] 
model_params.outlet_face_names = [outlet_face_name_RS, outlet_face_name_RC, outlet_face_name_LC, outlet_face_name_LS, outlet_face_name_DA] 
model_params.centerlines_file_name = os.path.join(input_dir, 'centerlines.vtp') 

# F: ============================================ FLUID PROPERTIES ============================================
fluid_props = params.FluidProperties()

# G: ============================================= WALL PROPERTIES ============================================
print("Set wall properties ...")
material = params.WallProperties.OlufsenMaterial()
print("Material model: {0:s}".format(str(material)))

# H: ========================================== SET BOUNDARY CONDITION ========================================
bcs = params.BoundaryConditions()
# H1: inlet flow wave form
bcs.add_velocities(face_name=inlet_face_name_AA, file_name=os.path.join(input_dir,flowwf_file_name))
# H2: outlet RCRs 
# H2a: arch branches
bcs.add_rcr(face_name=outlet_face_name_RS, Rp=4498.42, C=2.66239e-06, Rd=85470)
bcs.add_rcr(face_name=outlet_face_name_RC, Rp=4398.69, C=2.72275e-06, Rd=83575.2)
bcs.add_rcr(face_name=outlet_face_name_LC, Rp=4373.94, C=2.73816e-06, Rd=83104.8)
bcs.add_rcr(face_name=outlet_face_name_LS, Rp=4299.51, C=2.78556e-06, Rd=81690.7)
# H2b: descending aorta
bcs.add_rcr(face_name=outlet_face_name_DA, Rp=1517.72, C=7.89114e-06, Rd=28836.7)


# I: ========================================== SET SOLUTION PARAMETERS ======================================
solution_params = params.Solution()
solution_params.time_step = 0.0005
solution_params.num_time_steps = 660

# J: ======================================== WRITE SOLVER INPUT FILES =======================================
script_dir = '/Desktop/SimVascular/GeneralizedCoAmodel/PyInterface/Example01/simulation.py'
script_path = Path(os.path.realpath(script_dir)).parent
output_dir = str(script_path / 'output')
rom_simulation.write_input_file(model_order=1, model=model_params, mesh=mesh_params, fluid=fluid_props, material=material, boundary_conditions=bcs, solution=solution_params, directory=output_dir)









