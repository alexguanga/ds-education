import os
import json
from collections import defaultdict

'''Storing the current directory. '''


class SearchInformation:
    def __init__(self):
        self.current_path()

    def current_path(self):
        self.search_directory(os.getcwd())

    ''' Searches for the directory in the root list. '''
    def search_directory(self, path):
        root_list = []
        for root, dirs, files in os.walk(path):
            root_list.append(root)

        self.find_files(root_list)

    ''' Looks for the approrpiate file'''
    def find_files(self, root_directory):
        total_list = []

        for path in root_directory:
            if not self.search_ipynb_cp(path): # Ignoring files that are checkpoints
                for file in os.listdir(path):
                    if self.file_exists(file) is not None:
                        total_list.append(self.dir_file(path, file))

        markdownfiles = GetMarkdownInfo(total_list)

    ''' Returns file if its either a jupyter or R file'''
    def file_exists(self, file):
        if self.search_ipynb(file) or self.search_R(file):
            return file

    ''' We do not want files that are part of the checkpoint directory'''
    def search_ipynb_cp(self, path):
        return path.endswith(".ipynb_checkpoints")

    ''' Looks for jupyter file'''
    def search_ipynb(self, file):
        return file.endswith(".ipynb")

    ''' Looks for R file'''
    def search_R(self, file):
        return file.endswith(".R")

    ''' Merged absolute path w/ file:
            Returns a list: [fullpath w/ juypter file, fullpath w/o juypter file]'''
    def dir_file(self, path, file):
        path_file = path + '/' + file
        return path_file



class GetMarkdownInfo:
    ''' Converts juypter notebook to markdown. '''
    def __init__(self, total_list):
        self.total_list = total_list
        self.reading_files(self.total_list)

    def reading_files(self, total_list):
        all_json = self.extract_markdowns(total_list)
        total_list_files = self.include_all_files(total_list)
        sub_headers = self.markdown_subheaders(all_json)

        #CreateFrame(sub_headers)

    def frame_no_markdown(self, full_list):
        pass

    def include_all_files(self, total_list):
        clean_list = []
        for i in range(len(total_list)):
            clean_list.append(self.full_path_string(total_list[i]))
        return clean_list

    def full_path_string(self, pathname):
        return pathname[1]

    ''' Creates json and merges w/ path file.'''
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

    ''' Extracting the content from the markdown cells. '''
    def markdown_subheaders(self, headers):

        sub_headers = []
        for header in headers:
            new_path_name, new_file = self.scrape_file_info(header)
            all_sources_info = self.scrape_source_info(header)

            list_subheaders = []

            for source_info in all_sources_info:
                try:
                    topic = self.main_topic(source_info)
                    if self.main_topic(source_info) is not None:
                        list_subheaders.append(topic)

                    if [new_path_name, new_file, list_subheaders] not in sub_headers:
                        sub_headers.append([new_path_name, new_file, list_subheaders])
                except IndexError:
                    pass
        return sub_headers

    def appr_paths(self, single_file):
        return [single_file[0], single_file[1]]

    ''' Extract #1 Header from markdown. '''
    def markddown_files(self, json_format):
        for (key, value) in json_format.items():
            if type(value) is list: # juypter notebook contains additional dictionary which we do not need
                if value[0]['cell_type'] == "markdown":
                    return value

    def scrape_source_info(self, header):
        return header[0]

    def scrape_file_info(self, header):
        path_name = header[1]
        new_path, new_file = self.last_instance(path_name)
        return [new_path, new_file]

    def main_topic(self, source):
        topic = source['source'][0]
        if topic.startswith('#'):
            return self.cleaned_topic(topic)

    def cleaned_topic(self, topic):
        topic = topic.strip('#')
        topic = topic.lstrip()
        topic = topic.rstrip('\n')
        return topic

    ''' Returns last instance of /, which separates directories'''
    def last_instance(self, full_path):
        instance_pos = full_path.rfind('/')
        path = self.updated_pathname(full_path, instance_pos)
        file = self.updated_file(full_path, instance_pos)

        return [path, file]

    def updated_pathname(self, path, instance):
        return path[1:instance]

    def updated_file(self, path, instance):
        return path[instance+1:]



class CreateFrame:
    def __init__(self, topics):
        self.topics = topics
        framework_of_files = self.create_framework(topics)

    def create_framework(self, sub_headers_list):
        frame_d = self.rec_dd()

        for sub_header in sub_headers_list:
            main_topic, sub_topic, *rest_topics = self.split_headerlist(sub_header)
            check_validate = self.validate_topic(frame_d, main_topic, sub_topic)

            if (check_validate is True) and (rest_topics[0]):
                title = self.title_of_topic(rest_topics[0])
                frame_d[main_topic][sub_topic].append(rest_topics[0])

            elif (check_validate is False) and (rest_topics[0]):
                frame_d[main_topic][sub_topic] = rest_topics

        return frame_d

    def title_of_topic(self, topics):
        return topics[0]

    def split_headerlist(self, first_header):
        test_first_val = first_header # generalize for the rest of the vals

        path, first_cat, *subtopic = test_first_val
        init_path_val = self.extract_first_val(path)
        return[
            init_path_val, first_cat, *subtopic
        ]

    def rec_dd(self):
        return defaultdict(self.rec_dd)

    def validate_topic(self, frame_d, *args):
        m_topic, s_topic = args

        if m_topic in frame_d:
            if s_topic in frame_d[m_topic]: return True
            else: return False
        else: return False

    def extract_first_val(self, temp):
        return temp.split('/')[-1]


if __name__ == "__main__":
    SearchInformation()
