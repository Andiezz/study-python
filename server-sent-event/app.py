from flask import Flask, render_template, Response
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update-status')
def update_status():
    def generate():
        for i in range(5):
            yield f"data: Task {i} completed\n\n"
            time.sleep(10)  # Simulate long-running task
        yield "data: All tasks completed\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)