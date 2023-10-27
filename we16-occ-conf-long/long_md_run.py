import os

#-------------------------------location, folders, and run commands---------------------------------

#current location
cwd = os.getcwd()
run_dir = cwd.split("/")[-1]

#folders
input_folder = "input"
gen_script_folder = "run_scripts"
md_folder = "run_directory"

#create output and run folders
if not os.path.isdir(gen_script_folder):
	os.mkdir(gen_script_folder)
if not os.path.isdir(md_folder):
	os.mkdir(md_folder)

#run command files
run_prefix = 'r' # also used to name MD files
run_command_file_suffix = '_cmd.csh'
run_command_file_list = 'run_commands.txt'

gen_script_path = cwd + "/" + gen_script_folder + "/"

#-------------------------------simulation---------------------------------

#gromacs installation
gmx = "/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx"

#simulation input files
input_folder_path = cwd + "/" + input_folder + "/"

mdp_file 	  =	input_folder_path + "md"
topology_file = input_folder_path + "topol"
index_file 	  = input_folder_path + "index"
init_struct   = input_folder_path + "we-seg"

#production simulation command
#these differ only in having the arguments -r .gro vs -t .cpt
grompp_command_prod_init = "{gmx} grompp -f {mdp}.mdp -o {current}.tpr -c {previous}.gro -r {previous}.gro -p {topology}.top -n {index}.ndx -maxwarn 1\n"
grompp_command_prod 	 = "{gmx} grompp -f {mdp}.mdp -o {current}.tpr -c {previous}.gro -t {previous}.cpt -p {topology}.top -n {index}.ndx -maxwarn 1\n"
mdrun_command 			 = "{gmx} mdrun -v -deffnm {current} -ntomp 8 -ntmpi 1 -nb gpu -bonded gpu -pme gpu"

#-------------------------------generate commands---------------------------------

#number of serial simulations
n_segments = 100

#used to reference the output of the last md segment in gmx grompp
previous_sim = init_struct

for i in range(n_segments):

	#define simulation command
	current_sim = run_prefix + str(i).zfill(4)

	if i == 0:
		grompp_command = grompp_command_prod_init
	else:
		grompp_command = grompp_command_prod

	#simulation command file name
	sim_cmd_fn = current_sim + run_command_file_suffix

	#write simulation commands 
	with open(gen_script_path + sim_cmd_fn, 'w') as f:
		f.write(grompp_command.format(gmx = gmx, mdp = mdp_file, current = current_sim, previous = previous_sim, topology = topology_file, index = index_file))
		f.write( mdrun_command.format(gmx = gmx, 				 current = current_sim))

	#add run command files to list
	with open(gen_script_path + run_command_file_list, 'a') as f:
		f.write(sim_cmd_fn + '\n')
	
	#update previous sim
	previous_sim = current_sim


#---------------------concatenate trajectories after mdrun is finished---------------------

trjcat_cmd_fn = "trjcat_trjconv" + run_command_file_suffix

#write simulation commands 
with open(gen_script_path + trjcat_cmd_fn, 'w') as f:
	f.write(f"{gmx} trjcat -f eq*.trr -o eq-{run_dir}.xtc -cat")
	#f.write(f"{gmx} trjconv -s eq0.tpr -f eq-{run_dir}.xtc -pbc whole -o eq-{run_index}-whole.xtc") #does not work; needs user input

#add run command files to list
with open(gen_script_path + run_command_file_list, 'a') as f:
        f.write(trjcat_cmd_fn + '\n')


#submit a job which runs the commands written into the run_commands.txt file
os.chdir(md_folder)
print(os.getcwd())
os.system("qsub ../launch_job_array_production.sh %s" % run_dir) #with the arrow the script fails to process its argument
