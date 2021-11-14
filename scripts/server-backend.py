import subprocess

backend = '''
cd ../
cd backend
python3 app.py
'''

subprocess.Popen(backend, shell=True)