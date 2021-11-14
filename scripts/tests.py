import subprocess
import time

hardhat_server = '''
cd ../
cd blockchain
npx hardhat node
'''

test = '''
cd ../
cd blockchain
npx hardhat test --network localhost
'''

print('opening hardhat server...')
# using Popen to not wait for command to finish before moving to next line since server needs to be open
subprocess.Popen(hardhat_server, stdout=subprocess.DEVNULL, shell=True)
time.sleep(10)
subprocess.run(test, shell=True)