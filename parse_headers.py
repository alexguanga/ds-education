import os
import json
from collections import defaultdict
from reportlab.pdfgen import canvas
import numpy as np



'''
Class will compute the files that will be looked at

MIGHTS:
The user should be asked to comute the path they would like to use

Else: the current path should be used

IDEA: make the classs where only writes a file if the user wants

Another idea could be to look at the file and search info in the markdowns
'''
class SearchInformation:
    def __init__(self):
        self.current_path()

    def current_path(self):
        nearest_directories = self.nearest_dir()
        self.search_directory(os.getcwd())

    def nearest_dir(self):
        files = [f for f in os.listdir('.') if os.path.isdir(f)]
        return self.validate_dirs(files)

    def validate_dirs(self, files):
        dirs = []
        [dirs.append(f) for f in files if not f.startswith('.')]
        return dirs

    ''' Searches for the directory in the root list '''
    def search_directory(self, path):
        root_list = []
        for root, dirs, files in os.walk(path):
            root_list.append(root)

        self.find_files(root_list)

    ''' Looks for the approrpiate file '''
    def find_files(self, root_directory):
        total_list = []

        for path in root_directory:
            if not self.search_ipynb_cp(path): # Ignoring files that are checkpoints
                files_in_path = os.listdir(path)
                [total_list.append(self.dir_file(path, f)) for f in files_in_path if self.file_exists(f) is not None]

        markdownfiles = GetMarkdownInfo(total_list)

    def extract_req_files(self, path):
        pass

    ''' Returns file if its either a jupyter or R file '''
    def file_exists(self, file):
        if self.search_ipynb(file) or self.search_R(file):
            return file

    ''' We do not want files that are part of the checkpoint directory '''
    def search_ipynb_cp(self, path):
        return path.endswith(".ipynb_checkpoints")

    ''' Looks for jupyter file '''
    def search_ipynb(self, file):
        return file.endswith(".ipynb")

    ''' Looks for R file '''
    def search_R(self, file):
        return file.endswith(".R")

    ''' Merged absolute path w/ file:
            Returns a list: [fullpath w/ juypter file, fullpath w/o juypter file]'''
    def dir_file(self, path, file):
        path_file = path + '/' + file
        return [path, path_file]

class GetMarkdownInfo:
    ''' Converts juypter notebook to markdown. '''
    def __init__(self, total_list):
        self.total_list = total_list
        self.reading_files(self.total_list)

    ''' Computes the headers for the files'''
    def reading_files(self, total_list):
        all_json = self.extract_markdowns(total_list)
        sub_headers = self.markdown_subheaders(all_json)

        #CreateFrame(sub_headers)

    ''' Returning a list of all the files and their path (files that are not markdowns)'''
    def include_all_files(self, total_list):
        arranged_list = []
        for single_list in total_list:
            extract_filename = self.last_instance(single_list[1])
            extract_subdirectory = self.last_instance(extract_filename[0])
            arranged_data = self.array_info(extract_filename, extract_subdirectory)
            arranged_list.append(arranged_data)

        return arranged_list

    def array_info(self, app_file, app_dir):
        file_needed = app_file[1]
        path, subdir = app_dir
        return [path, subdir, [file_needed]]

    def full_path_string(self, pathname):
        return pathname[1]

    ''' Creates json and merges w/ path file.'''
    def extract_markdowns(self, compiled_list):
        all_json_files = []
        for single_file in compiled_list:
            path_name, path_name_file = self.appr_paths(single_file)

            with open(path_name_file) as filename:
                try:
                    json_file = self.upload_json(filename)
                    if json_file is not None:
                        all_json_files.append([json_file, path_name, path_name_file])

                except json.decoder.JSONDecodeError:
                    pass

        return all_json_files

    ''' Extracting the content from the markdown cells. '''
    def markdown_subheaders(self, headers):

        sub_headers = []
        for header in headers:
            list_subheaders = []
            update_path, new_file, source_info, file_header = self.parse_imp_data(header)

            list_subheaders.append(file_header)

            for source_info in source_info:
                try:
                    topic = self.main_topic(source_info)
                    if topic is not None:
                        list_subheaders.append(topic)

                    if [update_path, new_file, list_subheaders] not in sub_headers:
                        sub_headers.append([update_path, new_file, list_subheaders])
                except IndexError:
                    pass

        return sub_headers

    def parse_imp_data(self, header):
        new_path_name, new_file = self.scrape_file_info(header)
        all_sources_info = self.scrape_source_info(header)
        file_header = self.dir_filename(header)
        return [new_path_name, new_file, all_sources_info, file_header]

    def appr_paths(self, single_file):
        return [single_file[0], single_file[1]]

    def upload_json(self, filename):
        return self.markddown_files(json.load(filename))

    ''' Extract #1 Header from markdown. '''
    def markddown_files(self, json_format):
        for (key, value) in json_format.items():
            if type(value) is list: # juypter notebook contains additional dictionary which we do not need
                if value[0]['cell_type'] == "markdown":
                    return value

    def dir_filename(self, header):
        return header[2].split('/')[-1]

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
        return path[0:instance]

    def updated_file(self, path, instance):
        return path[instance+1:]


class CreateFrame:
    def __init__(self, topics):
        self.topics = topics
        framework_of_files = self.create_framework(topics)
        for f in framework_of_files:
            print(f)
        #BuildTemplate(framework_of_files)


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

        return [init_path_val, first_cat, *subtopic]

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


class BuildTemplate:
    def __init__(self, frame):
        self.frame = frame
        self.generate_pdf(frame)


    def generate_pdf(self, info):
        height_vals = self.pdf_topicrange(850, 100, 12)
        template = canvas.Canvas("Files_Strucuture.pdf")
        template.setFont('Helvetica', 8, leading=None)


        for counter, topic in enumerate(info):
            template.drawCentredString(100, height_vals[counter], str(topic))


            for s_counter, subtopic in enumerate(info[topic]):
                try:
                    pass #print (topic)
                    #print(height_vals[s_counter], height_vals[s_counter+1], len(height_vals), subtopic)
                    #height_vals = self.pdf_topicrange(height_vals[counter], height_vals[counter+1], len(height_vals))

                except IndexError:
                    pass
                #height_vals = self.pdf_topicrange(850, 100, 12)


        template.drawCentredString(250, 100, "TEMP")

        template.showPage()
        template.save()


    def pdf_topicrange(self, *args):
        highval, lowval, interval = args
        temp = np.linspace(highval, lowval, interval)
        return temp




if __name__ == "__main__":
    SearchInformation()
