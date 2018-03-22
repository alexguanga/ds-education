import os
import json
from collections import defaultdict

'''
Storing the directory
'''
def current_path():
    search_directory(os.getcwd())


'''
Searches for the directory in the root directory
'''
def search_directory(path):
    root_list = []
    for root, dirs, files in os.walk(path):
        root_list.append(root)

    searching_files(root_list) # 94 potential paths


'''
Extracting all files, and extract the exact path that include the juypter file
'''
def searching_files(current_dir):
    updated_paths = [] # The path without the juypter file
    paths_juypterfile = [] # The path including the juypter file
    all_files = []

    for path in current_dir:
        if not path.endswith('.ipynb_checkpoints'):
            for file_name in os.listdir(path):

                if file_name.endswith(".ipynb") or file_name.endswith(".R"):
                    updated_paths.append([path, file_name])

                    if file_name.endswith(".ipynb"):
                        include_juypter = dir_file(path, file_name)
                        paths_juypterfile.append(include_juypter)


    reading_files(updated_paths, paths_juypterfile)


'''
Converts juypter notebook to markdown
'''
def reading_files(all_path_info, juypter_path_info):
    for i in all_path_info:
        print(i)

    string_list = []
    for one_list in all_path_info:
        path_no_file = one_list[0]
        string_list.append(path_no_file.split('/')[4:])

    all_dict_paths = looping_dict(string_list)

    all_json = extract_markdowns(juypter_path_info)
    sub_headers = markdown_subheaders(all_json)

    #print(sub_headers)


'''
Creating the framework with dictionaries
'''
def looping_dict(complete_string_dir):
    all_dict_paths = {}

    for string_dir in complete_string_dir:
        current_level = all_dict_paths

        for part in string_dir:
            if part not in current_level:
                current_level[part] = {}

            current_level = current_level[part]

    return all_dict_paths


'''
Merged the absolute path with the file

Returns a list:
    [full path file including the juypter file, full path without the juypter file]
'''
def dir_file(path_no_file, juypter_file):
    path_and_file = path_no_file + '/' + juypter_file

    return [path_no_file, path_and_file]


'''
Creates the json file and merging it with the path file
Returns a list:
    [json file, the complete path file]
'''
def extract_markdowns(path_juypter_list):
    total_json_files = []

    for i in path_juypter_list:
        pathfile = i[0]
        pathfile_juypter = i[1]

        with open(pathfile_juypter) as juypter_name:
            file_to_json = json.load(juypter_name)
            json_file = markddown_files(file_to_json, pathfile)

            if json_file is not None:
                total_json_files.append([json_file, pathfile])

    return total_json_files


'''
Only want the juypter notebook if the first cell is a markdown
we do not want any code
'''
def markddown_files(json_format, file_name):
    for (key, value) in json_format.items():
        if type(value) is list: # juypter notebook contains additional dictionary which we do not need

            if value[0]['cell_type'] == "markdown":
                return value


'''
Extracting the content from the markdown cells
'''
def markdown_subheaders(headers):

    sub_headers = []
    for header in headers:
        file_path = header[1]
        last_instance = header[1].rfind('/') # looking for the last instance of /, which separates directories
        file_path_update = file_path[1:last_instance] # fixing the file path without the file in it
        juypter_file = file_path[last_instance+1:]

        source_headers = header[0]
        list_subheaders = []

        for source_header in source_headers:

            sub_header = source_header['source'][0]

            if sub_header.startswith('#'):

                sub_header = sub_header.strip('#')
                sub_header = sub_header.lstrip()
                sub_header = sub_header.rstrip('\n')
                list_subheaders.append(sub_header)
            if [file_path_update, juypter_file, list_subheaders] not in sub_headers:
                sub_headers.append([file_path_update, juypter_file, list_subheaders])

    return sub_headers








if __name__ == "__main__":
    current_path()
