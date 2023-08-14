upperdir2="/wynton/home/grabe/jborowsky/aac1/04-equil"
output_folder = "run_scripts/"

gmx = "/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx"

sim_command_minim = "{gmx} grompp -f {upperdir}/mdp/{mdp} -o {current}.tpr -c {previous}.gro -r {inp}.gro -p {upperdir}/input_structures/topol.top -n {upperdir}/input_structures/index.ndx -maxwarn 2 \n\
{gmx} mdrun -v -deffnm {current} -ntomp 4 -ntmpi 1"

sim_command_equil = "{gmx} grompp -f {upperdir}/mdp/{mdp} -o {current}.tpr -c {previous}.gro -r {inp}.gro -p {upperdir}/input_structures/topol.top -n {upperdir}/input_structures/index.ndx -maxwarn 2 \n\
{gmx} mdrun -v -deffnm {current} -ntomp 4 -ntmpi 1 -nb gpu -bonded gpu -pme gpu"

sim_command_prod  = "{gmx} grompp -f {upperdir}/mdp/{mdp} -o {current}.tpr -c {previous}.gro -t {previous}.cpt -p {upperdir}/input_structures/topol.top -n {upperdir}/input_structures/index.ndx -maxwarn 1 \n\
{gmx} mdrun -v -deffnm {current} -ntomp 4 -ntmpi 1 -nb gpu -bonded gpu -pme gpu"

file_prefix = 'step'
mdp_suffix = '_minimization.mdp'
file_suffix = '_run_cmd.csh'
initial_structure = '%s/input_structures/step5_input' % upperdir2

#Step names file:
runs_file = 'run_commands.txt'

#Step 6.0-6.6, minim and first equil:

#Step 6.0: minimization
#sim_prefix = 'minimization'
previous_sim = initial_structure
current_sim = "minimization"
current_mdp="minimcharmm36.mdp" #file_prefix+current_sim+mdp_suffix

with open(output_folder+file_prefix+current_sim+file_suffix, 'w') as f:
	f.write(sim_command_minim.format(gmx = gmx, upperdir = upperdir2, mdp=current_mdp, current=current_sim, previous=previous_sim, inp=initial_structure))
with open(output_folder+runs_file, 'a') as f:
	f.write(file_prefix+current_sim+file_suffix+'\n')

previous_sim = current_sim

#Step 6.1-6.6: short equilibration segments with different conditions
#mdp_suffix = '_equilibration.mdp'

mdp_files = ["nvtcharmm36.mdp", "npt01charmm36.mdp",  "npt02charmm36.mdp",  "npt03charmm36.mdp",  "npt04charmm36.mdp",  "npt05charmm36.mdp",  "npt06charmm36.mdp",  
	     "npt07charmm36.mdp", "npt07charmm36.mdp", "npt07charmm36.mdp",
		 "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp", "npt08charmm36.mdp"]

#n_equil_steps = len(mdp_files)-1

for i in range(0,len(mdp_files)):
	current_sim="eq"+str(i)
	current_mdp = mdp_files[i] #file_prefix+current_sim+mdp_suffix 
	with open(output_folder+file_prefix+current_sim+file_suffix, 'w') as f:
		f.write(sim_command_equil.format(gmx = gmx, upperdir = upperdir2, mdp=current_mdp, current=current_sim, previous=previous_sim, inp=initial_structure))
	with open(output_folder+runs_file, 'a') as f:
		f.write(file_prefix+current_sim+file_suffix+'\n')
	previous_sim = current_sim

#Step 6.7_0-10: long equilibration broken into segments sharing an mdp file
#sim_prefix = '6.7_'
#current_mdp = 'step6.7_equilibration.mdp'

#for i in range(2):
#	current_sim=sim_prefix+str(i)
#	with open(file_prefix+current_sim+file_suffix, 'w') as f:
#		f.write(sim_command_6.format(upperdir = upperdir2, mdp=current_mdp, current=current_sim, previous=previous_sim, inp=initial_structure))
#	with open(runs_file, 'a') as f:
#		f.write(file_prefix+current_sim+file_suffix+'\n')
#	previous_sim = current_sim

#Step 7, production:
#sim_prefix = '7_'
current_mdp = 'nptcharmm36.mdp'
for i in range(10):
	current_sim = str(i).zfill(3)
	
	with open(output_folder+file_prefix+current_sim+file_suffix, 'w') as f:
		f.write(sim_command_prod.format(gmx = gmx, upperdir = upperdir2, mdp=current_mdp, current=current_sim, previous=previous_sim))	
	with open(output_folder+runs_file, 'a') as f:
		f.write(file_prefix+current_sim+file_suffix+'\n')
	previous_sim = current_sim
