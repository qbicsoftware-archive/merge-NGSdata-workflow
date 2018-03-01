from CTDopts.CTDopts import _InFile, CTDModel, args_from_file
import sys
import os
import subprocess

def generate_outfile_name(identifier_split, strand):
	mate = {'forward': 'R1', 'reverse': 'R2'}

	if len(identifier_split) > 2:
		identifier = '%s_%s_merged_%s.fastq' % (identifier_split[0], identifier_split[1], mate[strand])
	else:
		identifier = '%s_merged_%s.fastq' % (identifier_split[0], mate[strand])

	return identifier 

wf_dir = sys.argv[1]
ctd_params = args_from_file(wf_dir + '/WORKFLOW-CTD')
ctd_files = args_from_file(wf_dir + '/IN-FILESTOSTAGE')

data_path = os.path.join(wf_dir, 'data')
result_path = os.path.join(wf_dir, 'result')
log_path = os.path.join(wf_dir, 'log')

for s in ['forward', 'reverse']:
	command = 'cat '

	for fi in ctd_files[s]:
		fileName = fi.split('/')[-1]
		if fi.endswith('.gz'):
			cmd = "gzip -d %s" % os.path.join(data_path, fileName)
			os.system(cmd)
			command += '%s ' %  os.path.join(data_path, fileName.replace('.gz', ''))
		else:
			command += '%s ' %  os.path.join(data_path, fileName)

	identifier_split = fileName.split('_')
	identifier = generate_outfile_name(identifier_split, s)
	outfile = os.path.join(result_path, identifier)
	command += '> %s' % outfile
	subprocess.call(command, shell=True)

