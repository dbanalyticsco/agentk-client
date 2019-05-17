import os
from flask import Flask, render_template, redirect, url_for, flash
import runner

app = Flask(__name__)
app.secret_key = 'DylanBaker'

JOBS_FILE = '../agentk/example_content/jobs.yml'
TEMPLATE_DIRECTORY = '../agentk/example_content'
LOOKER_BASE_URL = os.environ.get('LOOKER_BASE_URL')
LOOKER_CLIENT_ID = os.environ.get('LOOKER_CLIENT_ID')
LOOKER_CLIENT_SECRET = os.environ.get('LOOKER_CLIENT_SECRET')

def find_jobs():
	jobs = runner.find_jobs(JOBS_FILE)
	return jobs

def email(job_name):
	email = runner.run_job(JOBS_FILE, TEMPLATE_DIRECTORY, job_name, LOOKER_BASE_URL, LOOKER_CLIENT_ID, LOOKER_CLIENT_SECRET, port=19999)

@app.route("/jobs")
def jobs():
	
	jobs = find_jobs()
	print(jobs)

	return render_template('jobs.html', jobs=jobs)

@app.route("/send_email/<job_name>")
def send_email(job_name):

	email(job_name)
	flash('You successfully sent the job: {}'.format(job_name))
	return redirect(url_for('jobs'))



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)