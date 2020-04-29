#################
########   Final Project
#Name: Yanbo Shi
#Uniqname: yanboshi
#################

import sqlite3
from flask import Flask, render_template, request
import plotly.graph_objects as go 


def get_overall_results_for_universities():
    conn = sqlite3.connect('final_project.sqlite')
    cur = conn.cursor()
    q = '''
        SELECT Universities_in_states.UniversityName, Universities_in_states.State, Universities_in_states.NationalRank, University_details.SchoolType,University_details.ApplicationAcceptedRate,University_details.UniversityURL
        FROM Universities_in_states
        JOIN University_details
        ON Universities_in_states.UniversityName=University_details.Name
	    WHERE Universities_in_states.NationalRank BETWEEN 0 AND 100
	    ORDER BY Universities_in_states.NationalRank 
    '''
    overview_results = cur.execute(q).fetchall()
    conn.close()
    return overview_results


def get_results(state, schooltype, sort_type, sort_order):
    conn = sqlite3.connect('final_project.sqlite')
    cur = conn.cursor()

    q = f'''
        SELECT Universities_in_states.UniversityName, Universities_in_states.State, Universities_in_states.NationalRank, University_details.SchoolType,University_details.ApplicationAcceptedRate,
        University_details.StudentPopulation,University_details.AverageSalaryAfterTenYears,University_details.BachelorDegreeGraduationRate,University_details.UniversityURL
        FROM Universities_in_states
        JOIN University_details
        ON Universities_in_states.UniversityName=University_details.Name
	    WHERE Universities_in_states.State = '{state}' and University_details.SchoolType = '{schooltype}'
	    ORDER BY {sort_type} {sort_order}
	    LIMIT 7
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results




app = Flask(__name__)

@app.route('/overview')
def overview():
    results = get_overall_results_for_universities()
    return render_template('overview.html', results=results)

@app.route('/')
def name():
    return render_template('index.html')

@app.route('/state')
def state():
    return render_template('state.html')

@app.route('/state/results', methods=['POST'])
def state_results():
    state = request.form['state']
    schooltype = request.form['type']
    sort_type = request.form['sort']
    sort_order = request.form['dir']
    results = get_results(state, schooltype, sort_type, sort_order)
    return render_template('state_results.html', results=results)


@app.route('/state_plot')
def state_plot():
    return render_template('state_plot.html')

@app.route('/plot',methods=['POST'])
def plot():
    state = request.form['state']
    schooltype = request.form['type']
    sort_type = request.form['sort']
    sort_order = request.form['dir']
    results = get_results(state, schooltype, sort_type, sort_order)

    name = []
    ApplicationAcc = []
    Bachelor = []
    # studentpopu = []
    for item in results:
        name.append(item[0])
        ApplicationAcc.append(item[4])
        Bachelor.append(item[7])
        # studentpopu.append(item[5])

    Universities=name
    fig = go.Figure(data=[
        go.Bar(name='Applications Accepted Percentage', x=Universities, y=ApplicationAcc),
        go.Bar(name="Bachelor's Degree Graduation Rate", x=Universities, y=Bachelor),
        # go.Bar(name='Student Population', x=Universities, y=studentpopu)
    ])
    
    fig.update_layout(barmode='group')
    div = fig.to_html(full_html=False)
    return render_template("plot.html", plot_div=div)




if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)

