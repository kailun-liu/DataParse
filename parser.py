import os
import re
import xlsxwriter

for (dirpath, dirnames, filenames) in os.walk('./'):
	
	files = [file for file in os.listdir(dirpath) if file.endswith('.xoml')]

	for file in files:
		file_object = open(f'{dirpath}/{file}', 'rt', encoding='UTF-8')
		content = file_object.read()
		content_sections = content.split('</StateActivity>')
		retrieve_lists = []
		for content_section in content_sections:
			state = re.findall(r"(<StateActivity x:Name=.+)", content_section)
			
			if len(state)>1:
				for i in list(range(len(state))):
					state_value = state[i]
					state_value = state_value.split('\"')[1]
			else:
				try:
					state_value = state[0]
					state_value = state_value.split('\"')[1]
				except:
					state_value = 'No State Name'
				
			description_lists = re.findall(r"(<ns1:SymyxTransitionActivity.+)", content_section)
			description_lists = [item.split('\"')[1] for item in description_lists]
			if len(description_lists) == 0:
				description_lists.append("None")
			allowedactors_lists = re.findall(r"(AllowedActors=.+(?=\sRequiredSignature))", content_section)
			allowedactors_lists = [item.split('\"')[1] for item in allowedactors_lists]
			if len(allowedactors_lists) == 0 :
				allowedactors_lists.append("None")
			elif allowedactors_lists == "":
				allowedactors_lists.append("No Specified Actor")
			state_lists = [state_value for i in range(len(description_lists))]
			transition_lists = list(zip(state_lists, description_lists, allowedactors_lists))
			for transition_list in transition_lists:
				retrieve_lists.append(transition_list)
		workbook = xlsxwriter.Workbook(f'{file}'+".xlsx")
		worksheet = workbook.add_worksheet()
		bold = workbook.add_format({'bold': True})
		worksheet.write('A1', 'State', bold)
		worksheet.write('B1', 'Description', bold)
		worksheet.write('C1', 'AllowedActors', bold)
		row = 1
		col = 0
		for state, description, allowedactors in retrieve_lists:
			worksheet.write(row, col, state)
			worksheet.write(row, col+1, description)
			if allowedactors == "":
				allowedactors = "No Specified Actor"
			worksheet.write(row, col + 2, allowedactors)
			row += 1
		workbook.close()
		file_object.close()



	

