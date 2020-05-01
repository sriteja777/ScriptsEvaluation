from flask import Flask, render_template, redirect, url_for, request, make_response
import csv
import pandas as pd
app = Flask(__name__)
app.secret_key = 'scripts'

app.config.update(
    DEBUG=True,
    )

data = []
with open('static/Marks.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)


def get_next_script():
    global data
    ind = -1
    for i, r in enumerate(data[1:]):
        if r[2] == '0':
            ind = i+1
            break
    if ind == -1:
        return None
    usn = data[ind][0]
    name = data[ind][1]
    noq = len(data[0]) - 3
    questions = data[0][3:]
    file_data = {"usn": usn, "name": name, "path": "answer_scripts/" + usn + ".pdf", "ind": ind ,"noq": noq, "questions": questions}
    return file_data


@app.route('/')
def index():
    print('came index')
    return redirect(url_for('evaluation'))


def write_marks(ind, usn, marks):
    global data
    if data[ind][0] != usn:
        return -1
    data[ind][2] = '1'
    for i, mark in enumerate(marks):
        data[ind][3+i] = str(mark)
    with open('static/Marks.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


@app.route('/evaluation/', methods=['GET', 'POST'])
def evaluation():
    print('came evaluation')

    file = get_next_script()
    if file is None:
        return render_template("completed.html")
    return render_template("index.html", file_data=file)


@app.route('/submit', methods=["POST"])
def submit():
    ind = int(request.form["ind"])
    marks = []
    usn = request.form["usn"]
    noq = int(request.form["noq"])
    for i in range(1,noq+1):
        marks.append(request.form['q'+str(i)])
    print('marks', marks)
    write_marks(ind, usn, marks)
    return "ok"


@app.route('/marks')
def marks():
    df = pd.read_csv("static/Marks.csv")
    # fmt = lambda x: '{0:.2f}'.format(x) if pd.notnull(x) else 'No marks'
    html = df.to_html( classes=["table-bordered", "table-striped", "table-hover", "table_class"], table_id="marks-table", index=False, na_rep="No marks", justify="center", border=1)
    return render_template("marks.html", table=html)



@app.route('/simple')
def simple():
    print("came hereeeeeee")
    return render_template("simple.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, threaded=True)