import os

cwd = os.getcwd()
run_index = cwd.split("/")[-1][3:]

input_folder = "input"
output_folder = "run_scripts/" # the folder to which to output the generated scripts, not the folder for md output
run_folder = "run_directory"
mdpdir = "mdp-aac1-adp"

if not os.path.isdir(output_folder):
	os.mkdir(output_folder)
if not os.path.isdir(run_folder):
	os.mkdir(run_folder)

#upperdir2="/wynton/home/grabe/jborowsky/aac1/04-equil"

gmx = "/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx"

sim_command_minim = "{gmx} grompp -f {upperdir}/{mdpdir}/{mdp} -o {current}.tpr -c {previous}.gro -r {inp}.gro -p ../{input_folder}/topol.top -n ../{input_folder}/index.ndx -maxwarn 2 \n\
{gmx} mdrun -v -deffnm {current} -ntomp 8 -ntmpi 1"

sim_command_equil = "{gmx} grompp -f {upperdir}/{mdpdir}/{mdp} -o {current}.tpr -c {previous}.gro -r {inp}.gro -p ../{input_folder}/topol.top -n ../{input_folder}/index.ndx -maxwarn 2 \n\
{gmx} mdrun -v -deffnm {current} -ntomp 8 -ntmpi 1 -nb gpu -bonded gpu -pme gpu"

sim_command_prod  = "{gmx} grompp -f {upperdir}/{mdpdir}/{mdp} -o {current}.tpr -c {previous}.gro -t {previous}.cpt -p ../{input_folder}/topol.top -n ../{input_folder}/index.ndx -maxwarn 1 \n\
{gmx} mdrun -v -deffnm {current} -ntomp 8 -ntmpi 1 -nb gpu -bonded gpu -pme gpu"

file_prefix = 'step'
mdp_suffix = '_minimization.mdp'
file_suffix = '_run_cmd.csh'
initial_structure = "../%s/step5_input" % input_folder 
#'%s/input_structures/step5_input' % upperdir2

#Step names file:
runs_file = 'run_commands.txt'

#Step 6.0-6.6, minim and first equil:

#Step 6.0: minimization
#sim_prefix = 'minimization'
previous_sim = initial_structure
current_sim = "minimization"
current_mdp="minimcharmm36.mdp" 
#file_prefix+current_sim+mdp_suffix

with open(output_folder+file_prefix+current_sim+file_suffix, 'w') as f:
	f.write(sim_command_minim.format(gmx = gmx, upperdir = cwd+"/..", mdpdir=mdpdir, mdp=current_mdp, current=current_sim, previous=previous_sim, inp=initial_structure, input_folder=input_folder))
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
	current_sim="eq" + str(i).zfill(2)
	current_mdp = mdp_files[i] #file_prefix+current_sim+mdp_suffix 
	with open(output_folder+file_prefix+current_sim+file_suffix, 'w') as f:
		f.write(sim_command_equil.format(gmx = gmx, upperdir = cwd+"/..", mdpdir=mdpdir, mdp=current_mdp, current=current_sim, previous=previous_sim, inp=initial_structure, input_folder=input_folder))
	with open(output_folder+runs_file, 'a') as f:
		f.write(file_prefix+current_sim+file_suffix+'\n')
	previous_sim = current_sim

#concatenate and remove pbc from trajectories
with open(output_folder+"trjcat_trjconv"+file_suffix, 'w') as f:
	f.write("/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx trjcat -f eq*.trr -o eq-run%s.xtc -cat" % run_index)
	#f.write(f"/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx trjconv -s eq0.tpr -f eq-run{run_index}.xtc -pbc whole -o eq-{run_index}-whole.xtc")
with open(output_folder+runs_file, 'a') as f:
        f.write("trjcat_trjconv"+file_suffix+'\n')

#/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx trjcat -f eq*.trr -o eq_run08.trr -cat

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
#current_mdp = 'nptcharmm36.mdp'
#for i in range(10):
#	current_sim = str(i).zfill(3)
#	
#	with open(output_folder+file_prefix+current_sim+file_suffix, 'w') as f:
#		f.write(sim_command_prod.format(gmx = gmx, upperdir = cwd+"/..", mdpdir=mdpdir, mdp=current_mdp, current=current_sim, previous=previous_sim, input_folder=input_folder))	
#	with open(output_folder+runs_file, 'a') as f:
#		f.write(file_prefix+current_sim+file_suffix+'\n')
#	previous_sim = current_sim

os.chdir(run_folder)
#print("qsub < ../../scripts/launch_job_array.sh %s" % run_index)
os.system("qsub ../../scripts/launch_job_array.sh %s" % run_index) #with the arrow the script fails to process its argument
