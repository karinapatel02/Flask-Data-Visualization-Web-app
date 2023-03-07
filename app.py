from flask import Flask, request, render_template
import pyodbc



conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=;Pwd=;Encrypt=;TrustServerCertificate=;Connection Timeout=30;')

curr = conn.cursor()

app = Flask(__name__)

@app.route('/')
def display():
    return render_template("index.html")

@app.route('/query1', methods=['POST','GET'])
def query1():
    curr.execute("SELECT * FROM(SELECT count(mag) as 'mag < 1' FROM all_month WHERE all_month.mag < 1.0) AS Cloumn1,(SELECT count(mag) as 'mag 1 to 2' FROM all_month WHERE all_month.mag BETWEEN '1' AND '2') AS Column2,(SELECT count(mag) as 'mag 2 to 3' FROM all_month WHERE all_month.mag BETWEEN '1' AND '2') AS Column3,(SELECT count(mag) as 'mag 3 to 5' FROM all_month WHERE all_month.mag BETWEEN '1' AND '2') AS Column4;")
    q1 = curr.fetchall()
    y = [list(i[0:]) for i in q1]
    return render_template("query1.html", y = y[0])

@app.route('/query2', methods=['POST','GET'])
def query2():
    mag = float(request.form['mag'])
    curr.execute("SELECT * FROM(SELECT count(*) as 'Mag Inputed' FROM all_month WHERE all_month.mag > "+str(mag)+") AS Cloumn1,(SELECT count(*) as 'Rest of the mag' FROM all_month) AS Column2;")
    q1 = curr.fetchall()
    y = [list(i[0:]) for i in q1]
    print(y)
    return render_template("query2.html", y = y[0], mag = str(mag))

@app.route('/query3', methods=['POST','GET'])
def query3():
    curr.execute("SELECT TOP (100) mag as 'Mag' FROM all_month;")
    q1 = curr.fetchall()
    curr.execute("SELECT TOP(100) depth as 'Depth' FROM all_month;")
    q2 = curr.fetchall()
    y = [list(i[0:]) for i in q1]
    y1 = [list(i[0:]) for i in q2]
    mag = [j for sub in y for j in sub]
    depth = [j for sub in y1 for j in sub]
    qy3 = []
    for h, w in zip(mag, depth):
        qy3.append({'x': h, 'y': w})
    return render_template("query3.html", qy3 = qy3)

@app.route('/query4', methods=['POST','GET'])
def query4():
    mag = float(request.form['mag'])
    curr.execute("SELECT * FROM (SELECT count(mag) as '12:00AM' FROM all_month WHERE all_month.time LIKE '%T00%' AND all_month.mag >= "+str(mag)+") AS Column1, (SELECT count(mag) as '1:00AM' FROM all_month WHERE all_month.time LIKE '%T01%' AND all_month.mag >= "+str(mag)+") AS Column2, (SELECT count(mag) as '2:00AM' FROM all_month WHERE all_month.time LIKE '%T02%' AND all_month.mag >= "+str(mag)+") AS Column3, (SELECT count(mag) as '3:00AM' FROM all_month WHERE all_month.time LIKE '%T03%' AND all_month.mag >= "+str(mag)+") AS Column4, (SELECT count(mag) as '4:00AM' FROM all_month WHERE all_month.time LIKE '%T04%' AND all_month.mag >= "+str(mag)+") AS Column5, (SELECT count(mag) as '5:00AM' FROM all_month WHERE all_month.time LIKE '%T05%' AND all_month.mag >= "+str(mag)+") AS Column6;")
    q1 = curr.fetchall()
    y = [list(i[0:]) for i in q1]
    print(y)
    return render_template("query4.html", qy4 = y[0])

@app.route('/query5', methods=['POST','GET'])
def query5():
    r1 = float(request.form['r1'])
    r2 = float(request.form['r2'])
    curr.execute("SELECT net, count(mag) as 'Number of Magnitude' FROM all_month WHERE mag BETWEEN "+str(r1)+" AND "+str(r2)+" GROUP BY net;")
    q1 = curr.fetchall()
    y = [list(i[0:]) for i in q1]
    qy6 = y[:][:]
    labels = [i[:][0] for i in q1]
    data = [i[:][1] for i in q1]
    print(qy6)
    print(labels)
    print(data)
    return render_template("query5.html", qy6 = qy6, labels = labels, data = data)

if __name__ == "__main__":
    app.run()

