from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    with open('static/county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    if 'State' in request.args:
        selected_state = request.args["State"]
        return render_template('home.html', response_options = get_state_options(counties), response_percentage = get_average_hispanic_percentage(counties, selected_state), response_state = selected_state)
    return render_template('home.html', response_options = get_state_options(counties))

def get_state_options(counties):
    states = []
    options = ""
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
            options += Markup("<option value=\"" + c["State"] + "\">" + c["State"] + "</option>")
    return options

def get_average_hispanic_percentage(counties, selected_state):
    average_percent_hispanic = []
    for c in counties:
        if c["State"] == selected_state:
            average_percent_hispanic.append(c["Ethnicities"]["Hispanic or Latino"])
    
    return str(sum(average_percent_hispanic) / len(average_percent_hispanic))

if __name__=="__main__":
    app.run(debug=False, port=54321)
