import databasehandler
import collections
import time
from datetime import datetime
from flask import Flask, request, jsonify, Markup, render_template

#instance tridy pro praci s db
db = databasehandler.DatabaseHandler()

if __name__ == "__main__":
    app.run()

app = Flask(__name__)

#prijem dat z raspberry a ulozeni do db
@app.route('/api', methods=['POST'])
def index():
    data = request.json
    print(data['time'])
    print(data['increase'])
    db.insert_row(data['time'], data["increase"])
    
#zavola se po nacteni stranky s aktualnim datumem
@app.route('/graph', methods=['GET'])
def graph():
    total=db.count_total()
    date = datetime.today()
    selected_day=db.select_day(date.day,date.month,date.year)
    bar_values = []
    bar_labels = []
    hour_dict = {}
    for key in selected_day:
        if time.strftime("%H", time.localtime(key)) in hour_dict:
            hour_dict[time.strftime("%H", time.localtime(key))] = hour_dict[time.strftime("%H", time.localtime(key))] + selected_day[key]
        else:
            hour_dict[time.strftime("%H", time.localtime(key))] = selected_day[key]
    max_day_value = 0
    day_total=0
    for hour in hour_dict:
        value=hour_dict[hour]
        bar_labels.append(hour)
        bar_values.append(value)
        day_total=day_total+value
        if max_day_value < value:
            max_day_value = value
    print(bar_labels)
    print(bar_values)
    return render_template('bar_chart.html', title='Výroba energie: ' + str(date.day) + '.' + str(date.month) + '.' + str(date.year), max=max_day_value + max_day_value / 10, labels=bar_labels, values=bar_values, day_total='Vyrobeno za den: '+str(day_total),total='Vyrobeno celkem: '+str(total))


#zavola se pote co ozivatel zvoli datum
@app.route('/graph', methods=['POST'])
def graph_post():
    try:
        total=db.count_total()
        date = request.form['date'].split('-')
        selected_day=db.select_day(int(date[2]),int(date[1]),int(date[0]))
        bar_values = []
        bar_labels = []
        hour_dict = {}
        for key in selected_day:
            if time.strftime("%H", time.localtime(key)) in hour_dict:
                hour_dict[time.strftime("%H", time.localtime(key))] = hour_dict[time.strftime("%H", time.localtime(key))] + selected_day[key]
            else:
                hour_dict[time.strftime("%H", time.localtime(key))] = selected_day[key]       
        max_day_value = 0
        day_total=0
        for hour in hour_dict:
            value=hour_dict[hour]
            bar_labels.append(hour)
            bar_values.append(value)
            day_total=day_total+value
            if max_day_value < value:
                max_day_value = value
        print(bar_labels)
        print(bar_values)
        return render_template('bar_chart.html', title='Výroba energie: ' + date[2] + '.' + date[1] + '.' + date[0], max=max_day_value + max_day_value / 10, labels=bar_labels, values=bar_values, day_total='Vyrobeno za den: '+str(day_total),total='Vyrobeno celkem: '+str(total))
    except:
        return graph()
        
    
