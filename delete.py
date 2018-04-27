import os
import json
from collections import defaultdict

'''Storing the current directory. '''
def current_path():
    search_directory(os.getcwd())


''' Searches for the directory in the root list. '''
def search_directory(path):
    root_list = []
    for root, dirs, files in os.walk(path):
        root_list.append(root)

    searching_files(root_list) # 94 potential paths

def searching_files(current_dir):
    updated_paths = [] # The path without the juypter file
    paths_juypterfile = [] # The path including the juypter file

    for path in current_dir:
        if not search_ipynb_cp(path):
            for file in os.listdir(path):

                if search_ipynb(file) or search_R(file):

                    include_juypter = dir_file(path, file)
                    paths_juypterfile.append(include_juypter)
    reading_files(updated_paths, paths_juypterfile)

def search_files(path):
    for file in os.listdir(path):
        file_info = file_exists(file)
        return [file_info, path]

def file_exists(file):
    if search_ipynb(file) or search_R(file):
        return file

def search_ipynb_cp(path):
    return path.endswith('.ipynb_checkpoints')

def search_ipynb(file):
    return file.endswith(".ipynb")

def search_R(file):
    return file.endswith(".R")



''' Converts juypter notebook to markdown. '''
def reading_files(all_path_info, juypter_path_info):

    '''string_list = []
    for one_list in all_path_info:
        path_no_file = one_list[0]
        string_list.append(path_no_file.split('/')[4:])
    '''

    all_json = extract_markdowns(juypter_path_info)
    sub_headers = markdown_subheaders(all_json)
    create_framework(sub_headers)

    # Use sub_headers to create a framework dictionary
def create_framework(sub_headers_list):

    frame_d = rec_dd()

    for sub_header in sub_headers_list:
        main_topic, sub_topic, *rest_topics = split_headerlist(sub_header)
        check_validate = validate_topic(frame_d, main_topic, sub_topic)

        if check_validate is True:
            frame_d[main_topic][sub_topic].append(rest_topics[0])

        elif check_validate is False:
            frame_d[main_topic][sub_topic] = rest_topics



def validate_topic(frame_d, *args):
    m_topic, s_topic = args

    if m_topic in frame_d:
        if s_topic in frame_d[m_topic]: return True
        else: return False
    else: return False



def rec_dd():
    return defaultdict(rec_dd)



def split_headerlist(first_header):
    test_first_val = first_header # generalize for the rest of the vals

    path, first_cat, *subtopic = test_first_val
    init_path_val = extract_first_val(path)
    return[
        init_path_val, first_cat, *subtopic
    ]

def extract_first_val(temp):
    return temp.split('/')[-1]


''' Merged the absolute path with the file

Returns a list:
    [full path file including the juypter file, full path without the juypter file] '''

def dir_file(path_no_file, juypter_file):
    path_and_file = path_no_file + '/' + juypter_file

    return [path_no_file, path_and_file]


''' Creates the json file and merging it with the path file.

Returns a list:
    [json file, the complete path file]'''

def extract_markdowns(path_juypter_list):
    total_json_files = []

    for i in path_juypter_list:
        pathfile = i[0]
        pathfile_juypter = i[1]

        with open(pathfile_juypter) as juypter_name:
            try:
                file_to_json = json.load(juypter_name)
                json_file = markddown_files(file_to_json, pathfile)

                if json_file is not None:
                    total_json_files.append([json_file, pathfile])
            except json.decoder.JSONDecodeError:
                pass

    return total_json_files


''' Only want the juypter notebook if the first cell is a markdown. '''
def markddown_files(json_format, file_name):
    for (key, value) in json_format.items():
        if type(value) is list: # juypter notebook contains additional dictionary which we do not need

            if value[0]['cell_type'] == "markdown":
                return value


''' Extracting the content from the markdown cells. '''
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
            try:
                sub_header = source_header['source'][0]


                if sub_header.startswith('#'):

                    sub_header = sub_header.strip('#')
                    sub_header = sub_header.lstrip()
                    sub_header = sub_header.rstrip('\n')
                    list_subheaders.append(sub_header)

                if [file_path_update, juypter_file, list_subheaders] not in sub_headers:
                    sub_headers.append([file_path_update, juypter_file, list_subheaders])
            except IndexError:
                pass
    print(sub_headers)
    return sub_headers








if __name__ == "__main__":
    current_path()



'''def extract_allfiles(self, compiled_list):
        all_files = []
        for file in compiled_list:
            path_name, path_name_file = self.appr_paths(single_file)

    def search_infile(self, p_withname):
        with open(p_withname) as file:
            try:
                file_to_json = json.load(filename)
                json_file = self.markddown_files(file_to_json)

                if json_file is not None:
                    all_json_files.append([json_file, path_name])
'''





"""
def extract_markdowns(self, compiled_list):
        all_json_files = []

        for single_file in compiled_list:
            path_name, path_name_file = self.appr_paths(single_file)

            with open(path_name_file) as filename:
                try:
                    file_to_json = json.load(filename)
                    json_file = self.markddown_files(file_to_json)

                    if json_file is not None:
                        all_json_files.append([json_file, path_name])

                except json.decoder.JSONDecodeError:
                    pass
        return all_json_files

def extract_files(self, compiled_list):
        all_files = []
        for file in compiled_list:
            path_name, path_name_file = self.appr_paths(file)
            json_file = self.open_pathfile(path_name_file)
            print([json_file, path_name])
            all_files.append([json_file, path_name])

        return all_files

    def open_pathfile(self, path_name_file):
        with open(path_name_file) as file:
            try:
                file_to_json = json.load(file)
                json_file = self.markddown_files(file_to_json)


                if json_file is not None:
                    return json_file
            except json.decoder.JSONDecodeError:
                pass


"""
