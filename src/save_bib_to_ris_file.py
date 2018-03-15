
import os

def save_bib_to_ris_file(bib_data_arr, output_file):

	bib_data_arr = bib_data_arr[0].split('\n\n')  ## save "@proceedings" or "@inproceedings"

	with open(output_file, 'a+') as file_out:

		#while bib_data_arr.pop()
		bib_data_arr=bib_data_arr[0].split('},\n')
		for i in range(len(bib_data_arr)):
			if bib_data_arr[i].strip().startswith('@'):
				line_arr=bib_data_arr[i].strip().split(',\n')
				if line_arr[0].strip().startswith('@proceedings'):
					line_str = 'TY  - CONF'+'\n'
					line_str += 'LB  - ' + line_arr[0].split('{')[-1]+'\n'
					#file_out.write(line_str + '\n')
				elif line_arr[0].strip().startswith('@inproceedings'):
					line_str = 'TY  - CONF'+'\n'
					line_str += 'LB  - ' + line_arr[0].split('{')[-1]+'\n'
				else:
					pass
				if line_arr[1].strip().strip('\t').startswith('editor'):
					line_str += 'A2  - ' + line_arr[1].split('{')[-1]
					#file_out.write(line_str + '\n')
				elif  line_arr[1].strip().strip('\t').startswith('author'):
					line_str += 'AU  - ' + line_arr[1].split('{')[-1]
				else:
					pass
			elif bib_data_arr[i].strip().strip('\t').startswith('title'):
				line_str = 'TI  - ' + bib_data_arr[i].split('=')[-1][2:]
				#file_out.write(line_str + '\n')
			elif bib_data_arr[i].strip().strip('\t').startswith('year'):
				line_str = 'PY  - ' + bib_data_arr[i].split('=')[-1][2:]
				#file_out.write(line_str + '\n')
			elif bib_data_arr[i].strip().strip('\t').startswith('url'):
				line_str = 'UR  - ' + bib_data_arr[i].split('{')[-1]
				#file_out.write(line_str + '\n')
			elif bib_data_arr[i].strip().strip('\t').startswith('isbn'):
				line_str = 'SN  - ' + bib_data_arr[i].split('=')[-1][2:]
				#file_out.write(line_str + '\n')
			elif bib_data_arr[i].strip().strip('\t').startswith('biburl'):
				line_str = 'DP  - ' + bib_data_arr[i].split('=')[-1][2:]
				#file_out.write(line_str + '\n')
			elif bib_data_arr[i].strip().strip('\t').startswith('publisher'):
				line_str = 'PB  - ' + bib_data_arr[i].split('=')[-1][2:]
				#file_out.write(line_str + '\n')
			elif bib_data_arr[i].strip().strip('\t').startswith('booktitle'):
				line_str = 'C3  - ' + bib_data_arr[i].split('=')[-1][2:]
			elif bib_data_arr[i].strip().strip('\t').startswith('pages'):
				line_str = 'SP  - ' + bib_data_arr[i].split('=')[-1][2:]
			elif bib_data_arr[i].strip().strip('\t').startswith('doi'):
				line_str = 'DO  - ' + bib_data_arr[i].split('=')[-1][2:]
			elif bib_data_arr[i].strip().strip('\t').startswith('bibsource'):
				line_str = 'DB  - ' + bib_data_arr[i].split('=')[-1].split('}\n')[0][2:]
			else:
				continue
				#pass
			print(line_str)
			file_out.write(line_str + '\n')
			line_str=''

		line_str = 'ER  -  \n'
		file_out.write(line_str + '\n')
			# 	file_out.write(str.encode(line_str + '\n', 'utf-8'))


		# file_out.write(line + '\n')
		# if line.strip().startswith('@'):
		# 	line_arr = line.split('{')
		# 	# label=os.path.join(label_dir_path,line_arr[1][:-1])
		# 	label = 'internal-pdf://../' + os.path.join(sub_dir, line_arr[1][:-1])
		# 	line_str = 'LB  - ' + line_arr[1][:-1]
		# 	file_out.write(str.encode(line_str + '\n', 'utf-8'))
		# if line.strip().startswith('@InProceedings'):
		# 	line_str = 'TY  - ' + 'CONF'
		# else:
		# 	line_arr = line.strip().strip('\t').split('=')
		# 	if len(line_arr) < 2:
		# 		if line.strip().startswith('}'):
		# 			line_str = 'L1  - ' + label + '.pdf' + '\n'
		# 			line_str += 'L1  - ' + label + '-supp' + '.pdf' + '\n'
		# 			line_str += 'ER  -  \n'
		# 			file_out.write(str.encode(line_str + '\n', 'utf-8'))
		# 		line = file_in.readline()
		# 		continue
		# 	for i in range(len(line_arr[1])):
		# 		# print('i=',i)
		# 		if line_arr[1][i] == '{':
		# 			value = line_arr[1][i + 1:-2]
		# 			break
		# 	# if 'title ='in line:
		# 	if line.strip().startswith('title = '):
		# 		# line_arr = line.split('{')
		# 		line_str = 'TI  - ' + value
		# 	if line.strip().startswith('author = '):
		# 		# line_arr = line.split('{')
		# 		line_str = 'AU  - ' + value
		# 	if line.strip().startswith('abstract = '):
		# 		# line_arr = line.split('{')
		# 		line_str = 'AB  - ' + value
		# 	if line.strip().startswith('pages = '):
		# 		line_str = 'SP  - ' + value
		# 	if line.strip().startswith('year = '):
		# 		line_str = 'PY  - ' + value
		# 	if line.strip().startswith('url = '):
		# 		line_str = 'UR  - ' + value
		# 	if line.strip().startswith('doi = '):
		# 		line_str = 'DO  - ' + value
		# 	if line.strip().startswith('volume = '):
		# 		line_str = 'VL  - ' + value
		# 	if line.strip().startswith('publisher = '):
		# 		line_str = 'PB  - ' + value
		# 	if line.strip().startswith('editor = '):
		# 		line_str = 'A2  - ' + value
		# 	if line.strip().startswith('series = '):
		# 		line_str = 'T3  - ' + value
		# 	if line.strip().startswith('booktitle = '):
		# 		line_str = 'C3  - ' + value
		# 	if line.strip().startswith('address = '):
		# 		line_str = 'CY  - ' + value
		# 	if line.strip().startswith('month = '):
		# 		line_str = 'DA  - ' + value
		# 	if line.strip().startswith('pdf = '):
		# 		line_str = 'OP  - ' + value
		# # print("==",line_str, line_arr[1])
		# # print(line_str)
		# file_out.write(str.encode(line_str + '\n', 'utf-8'))
