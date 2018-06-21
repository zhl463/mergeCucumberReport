import json
import glob
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
output_list = []
read_files = glob.glob(os.path.join(ROOT_DIR, "./target/P01/*.json"))


def merge_first_run_json():
    for f in read_files:
        with open(f, "rb") as infile:
            output_list.append(json.load(infile))

        with open(os.path.join(ROOT_DIR, "./merged/merged_file.json"), "wb") as outfile:
            json.dump(output_list, outfile)


def read_rerun_json():
    read_rerun_file = open(os.path.join(ROOT_DIR, "./target/json-reports/cucumber.json"), "rb")
    load_rerun = json.load(read_rerun_file)

    for first_run_json in read_files:
        with open(first_run_json, "rb") as f_run:
            load_first_run = json.load(f_run)
            for rerun_json in load_rerun:

                if rerun_json['uri'].encode('utf8') == load_first_run[0]['uri'].encode('utf8'):
                    ele = rerun_json['elements']
                    tmp = run_ele = load_first_run[0]['elements']
                    last_element = []
                    # length = len(load_first_run[0]['elements'])
                    for index in range(0, (len(ele) if len(ele) == 1 else len(ele) - 1)):
                        for run_index in range(0, len(run_ele) - 1):
                            if run_ele[run_index]['line'] == ele[index]['line']:
                                append_element = ele[index]
                                last_element.append(append_element)
                                tmp.pop(run_index)
                        for data in tmp:
                            last_element.append(data)

                    with open(first_run_json, 'wb') as m:
                        del load_first_run[0]['elements']
                        load_first_run[0]['elements'] = last_element
                        m.write(json.dumps(load_first_run))


def read_first_json():
    read_first_file = open(os.path.join(ROOT_DIR, "./merged/merged_file.json"), "rb")
    first_data = json.load(read_first_file)
    return first_data


if __name__ == '__main__':
    # merge_first_run_json()
    read_rerun_json()
