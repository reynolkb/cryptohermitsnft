import subprocess

frontend = '''
cd ../
cd frontend
npm start
'''

subprocess.Popen(frontend, shell=True)