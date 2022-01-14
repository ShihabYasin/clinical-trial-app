import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from datetime import datetime
from shutil import copyfile


'''
Category Mapping:
 RIPC == Generic Count
 Sham == Controlled Count
 
'''


PROJECT_ROOT = os.path.dirname (os.path.realpath (__file__))

app = Flask (__name__)
CORS (app)


class Todo (object):
    def __init__(self, name: str, controlled: int, generic: int):
        self.name = name
        self.controlled = controlled
        self.generic = generic
        self.generic = generic


# Utility
def ConvertListToDict(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def replace_line(file_name, line_num, text):
    lines = open (file_name, 'r').readlines ()
    lines[line_num] = text
    out = open (file_name, 'w')
    out.writelines (lines)
    out.close ()


def get_todolist():
    # getting all db data - stat
    with open ('total_count.txt') as f:
        content = f.readlines ()
    content = [line.split ('\n')[0] for line in content]

    ## GET PREV STAT
    total_patient = int (content[5].split (' ')[1])
    # print (total_patient)

    controlled_diabetes = int (content[1].split (' ')[1])
    controlled_chronic_kidney_disease = int (content[2].split (' ')[1])
    controlled_anemia = int (content[3].split (' ')[1])
    controlled_heart_failure = int (content[4].split (' ')[1])

    generic_diabetes = int (content[1].split (' ')[2])
    generic_chronic_kidney_disease = int (content[2].split (' ')[2])
    generic_anemia = int (content[3].split (' ')[2])
    generic_heart_failure = int (content[4].split (' ')[2])

    diabetes_data = Todo (name='Diabetes', controlled=controlled_diabetes, generic=generic_diabetes)
    chronic_kidney_disease_data = Todo (name='Chronic Kidney Disease', controlled=controlled_chronic_kidney_disease, generic=generic_chronic_kidney_disease)
    anemia_data = Todo (name='Anemia', controlled=controlled_anemia, generic=generic_anemia)
    heart_failure_data = Todo (name='Heart Failure', controlled=controlled_heart_failure, generic=generic_heart_failure)

    todo_list = [diabetes_data, chronic_kidney_disease_data, anemia_data, heart_failure_data]
    return todo_list, total_patient

@app.route ("/delete/", methods=["GET", "POST"])
def delete():
    with open ('total_count.txt') as f:
        content = f.readlines ()

    ## some vars
    total_patient = int (content[5].split (' ')[1])
    time_stamp = datetime.now ()

    ## GET PREV STAT
    controlled_diabetes = int (content[1].split (' ')[1])
    controlled_chronic_kidney_disease = int (content[2].split (' ')[1])
    controlled_anemia = int (content[3].split (' ')[1])
    controlled_heart_failure = int (content[4].split (' ')[1])

    generic_diabetes = int (content[1].split (' ')[2])
    generic_chronic_kidney_disease = int (content[2].split (' ')[2])
    generic_anemia = int (content[3].split (' ')[2])
    generic_heart_failure = int (content[4].split (' ')[2])

    ## del
    last_record = 'no-data'
    content_record = []
    with open ('record.txt') as f2:
        content_record = f2.readlines ()
    if len (content_record) > 0:
        last_record = content_record[-1].strip('\n').replace(':','').split(' ')
    else:
        todo_list, total_patient = get_todolist ()
        return render_template ("index.html", total_patient=total_patient, todo_list=todo_list, category_list=[])

    last_record = last_record[2:]
    last_record_map = ConvertListToDict(last_record)

    if 'category' not in last_record_map:
        todo_list, total_patient = get_todolist ()
        return render_template ("index.html", total_patient=total_patient, todo_list=todo_list, category_list=[])

    print(last_record_map)

    if last_record_map['category'] == 'RIPC':
        generic_heart_failure = generic_heart_failure -  int(last_record_map['heart_failure'])
        generic_diabetes = generic_diabetes - int (last_record_map['diabetes'])
        generic_chronic_kidney_disease = generic_chronic_kidney_disease - int (last_record_map['chronic_kidney_disease'])
        generic_anemia = generic_anemia - int (last_record_map['anemia'])

    elif last_record_map['category'] == 'Sham':
        controlled_heart_failure = controlled_heart_failure - int (last_record_map['heart_failure'])
        controlled_diabetes = controlled_diabetes - int (last_record_map['diabetes'])
        controlled_chronic_kidney_disease = controlled_chronic_kidney_disease - int (last_record_map['chronic_kidney_disease'])
        controlled_anemia = controlled_anemia - int (last_record_map['anemia'])

    # return str(last_record_map), 200
    # write
    replace_line (file_name='total_count.txt', line_num=1, text='diabetes ' + str (controlled_diabetes) + ' ' + str (generic_diabetes) + '\n')
    replace_line (file_name='total_count.txt', line_num=2, text='chronic_kidney_disease ' + str (controlled_chronic_kidney_disease) + ' ' + str (generic_chronic_kidney_disease) + '\n')
    replace_line (file_name='total_count.txt', line_num=3, text='anemia ' + str (controlled_anemia) + ' ' + str (generic_anemia) + '\n')
    replace_line (file_name='total_count.txt', line_num=4, text='heart_failure ' + str (controlled_heart_failure) + ' ' + str (generic_heart_failure) + '\n')


    total_patient -= 1
    replace_line (file_name='total_count.txt', line_num=5, text='total_patient ' + str (total_patient) + '\n')
    copyfile ('record.txt', 'record_saved.txt')

    open("record.txt", "w").close()  # deleting old content

    for line in content_record[:-1]:
        print(line.strip('\n'), file=open('record.txt','a'))

    todo_list, total_patient = get_todolist ()
    return render_template ("delete.html", total_patient=total_patient, todo_list=todo_list, category_list=[])

@app.route ("/", methods=["GET", "POST"])
def add():
    diabetes = request.form.get ("diabetes")
    chronic_kidney_disease = request.form.get ("chronic_kidney_disease")
    anemia = request.form.get ("anemia")
    heart_failure = request.form.get ("heart_failure")

    if diabetes == 'diabetes':
        diabetes = 1
    else:
        diabetes = 0

    if chronic_kidney_disease == 'chronic_kidney_disease':
        chronic_kidney_disease = 1
    else:
        chronic_kidney_disease = 0

    if anemia == 'anemia':
        anemia = 1
    else:
        anemia = 0

    if heart_failure == 'heart_failure':
        heart_failure = 1
    else:
        heart_failure = 0

    print (heart_failure, anemia, chronic_kidney_disease, diabetes)

    if heart_failure == 0 and anemia == 0 and chronic_kidney_disease == 0 and diabetes == 0:
        todo_list, total_patient = get_todolist ()
        return render_template ("index.html", total_patient=total_patient, todo_list=todo_list, category_list=[])

    with open ('total_count.txt') as f:
        content = f.readlines ()

    ## some vars
    total_patient = int (content[5].split (' ')[1])
    time_stamp = datetime.now ()

    ## GET PREV STAT
    controlled_diabetes = int (content[1].split (' ')[1])
    controlled_chronic_kidney_disease = int (content[2].split (' ')[1])
    controlled_anemia = int (content[3].split (' ')[1])
    controlled_heart_failure = int (content[4].split (' ')[1])

    generic_diabetes = int (content[1].split (' ')[2])
    generic_chronic_kidney_disease = int (content[2].split (' ')[2])
    generic_anemia = int (content[3].split (' ')[2])
    generic_heart_failure = int (content[4].split (' ')[2])

    ########################

    total_diff_if_controlled = 0  # total_diff_if_controlled for new patient
    # if medicine applied , calc diff
    if diabetes:
        total_diff_if_controlled += 1 + controlled_diabetes - generic_diabetes

    if chronic_kidney_disease:
        total_diff_if_controlled += 1 + controlled_chronic_kidney_disease - generic_chronic_kidney_disease

    if anemia:
        total_diff_if_controlled += 1 + controlled_anemia - generic_anemia

    if heart_failure:
        total_diff_if_controlled += 1 + controlled_heart_failure - generic_heart_failure

    ########################

    total_diff_if_generic = 0  # total_diff_if_controlled for new patient
    # if medicine applied , calc diff
    if diabetes:
        total_diff_if_generic += 1 - controlled_diabetes + generic_diabetes

    if chronic_kidney_disease:
        total_diff_if_generic += 1 - controlled_chronic_kidney_disease + generic_chronic_kidney_disease

    if anemia:
        total_diff_if_generic += 1 - controlled_anemia + generic_anemia

    if heart_failure:
        total_diff_if_generic += 1 - controlled_heart_failure + generic_heart_failure

    category = 'none'

    if total_diff_if_controlled <= total_diff_if_generic:
        category = 'Sham'

        if diabetes:
            controlled_diabetes += 1

        if chronic_kidney_disease:
            controlled_chronic_kidney_disease += 1

        if anemia:
            controlled_anemia += 1

        if heart_failure:
            controlled_heart_failure += 1

    else:
        category = 'RIPC'

        if diabetes:
            generic_diabetes += 1

        if chronic_kidney_disease:
            generic_chronic_kidney_disease += 1

        if anemia:
            generic_anemia += 1

        if heart_failure:
            generic_heart_failure += 1

    # write
    replace_line (file_name='total_count.txt', line_num=1, text='diabetes ' + str (controlled_diabetes) + ' ' + str (generic_diabetes) + '\n')
    replace_line (file_name='total_count.txt', line_num=2, text='chronic_kidney_disease ' + str (controlled_chronic_kidney_disease) + ' ' + str (generic_chronic_kidney_disease) + '\n')
    replace_line (file_name='total_count.txt', line_num=3, text='anemia ' + str (controlled_anemia) + ' ' + str (generic_anemia) + '\n')
    replace_line (file_name='total_count.txt', line_num=4, text='heart_failure ' + str (controlled_heart_failure) + ' ' + str (generic_heart_failure) + '\n')
    total_patient += 1
    replace_line (file_name='total_count.txt', line_num=5, text='total_patient ' + str (total_patient) + '\n')

    decision_category = category

    print (str (time_stamp), 'diabetes: ' + str (diabetes), \
           'chronic_kidney_disease: ' + str (chronic_kidney_disease), \
           'anemia: ' + str (anemia), \
           'heart_failure: ' + str (heart_failure), \
           'category: ' + category, \
           file=open ('record.txt', 'a'))

    todo_list, total_patient = get_todolist ()
    category_list = [category]
    return render_template ("index.html", total_patient=total_patient, todo_list=todo_list, category_list=category_list)


if __name__ == "__main__":
    open ("record.txt", "w").close ()
    open ("total_count.txt", "w").close ()
    copyfile('clean_db.txt','total_count.txt')
    app.run (host='127.0.0.1', port=8693, debug=True)
