import subprocess

blockchain_dependencies = '''
cd ../
cd blockchain
npm install
'''

frontend_dependencies = '''
cd ../
cd frontend
npm install
'''

subprocess.run(blockchain_dependencies, shell=True)
subprocess.run(frontend_dependencies, shell=True)