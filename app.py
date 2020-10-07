from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def get_data():
    file = open("/home/pi/audioProject/apimode.txt","r")
    api = file.read().splitlines()
    Current_mode=api[0]
    file.close()
    file = open("/home/pi/audioProject/api.txt","r")
    api = file.read().splitlines()
    Last_time_run= api[0]
    last_file=api[1]
    last_file_date=api[2]
    Model=api[3]
    file.close()
    
    return render_template('index.html', Last_time_run=Last_time_run,
                           Current_mode=Current_mode,
                           last_file=last_file,
                           last_file_date=last_file_date,
                           Model=Model)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    