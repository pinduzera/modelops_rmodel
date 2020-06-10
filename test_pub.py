import docker
import socket
from contextlib import closing
import sys
import time

### defining function to find free port
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

### model and host options
modelname = 'r_auto_docker' ## all must be small

client = docker.DockerClient(base_url='tcp://localhost:2375')

# img_list = client.images.list()
# img_list

# image = client.images.list(filters={'reference':'127.0.0.1:5000/'+modelname})

## Find a free port

free_port = find_free_port()

### delete old container of same same
try:
  old_con = client.containers.get(modelname)
  old_con.stop()
  old_con.remove()
  print('Deleted old container with the same name')
except:
  print('No container has been removed')
  pass
  
#### Run the container
### here you can setup container limitations
### such as CPU usage
print('Running new container in port:' + str(free_port) )

container = client.containers.run('127.0.0.1:5000/'+modelname,
                                 ports = {'8080/tcp':str(free_port)},
                                 name = modelname,
                                 detach = True)

### otherwise it will
### try to copy the files before the
### container is actually ready
time.sleep(10)

### container info

print(container.attrs['Config'])


#### container model folders
exit_code, output = container.exec_run("ls",
                                      workdir = '/pybox/model')

print('Exit code list: ' + str(exit_code))
print(output.decode("utf-8"))

### There is a bug, MM has a standard _score.R file that must be
### substituted by your actual score code
### since this change is made inside the container when uploaded
### it must be changed everytime the container dies
### it's an workaround for first deployment
### not very reliable yet

exit_code, output = container.exec_run("cp scoreCode.R _score.R", 
                                        workdir = '/pybox/model')

print('Exit code copy: ' + str(exit_code))
print(output.decode("utf-8"))

exit_code, output = container.exec_run("cat _score.R",
                                      workdir = '/pybox/model')

print(output.decode("utf-8"))
##### Scoring

import requests
import pandas as pd
import io

host = 'localhost'


### make the first request the container sending the score file
with open('./data/hmeq_score.csv', 'rb') as f:
    r = requests.post("http://"+host+':'+str(free_port)+'/executions', files={'file': f})

r.json()

val = r.json()['id']

### request the output
r2 = requests.get("http://" + host + ':'+str(free_port)+'/query/' + val)

### print the output
df = pd.read_csv(io.BytesIO(r2.content))
df.head()

### check the log if there is an issu
r3 = requests.get("http://" + host + ':'+str(free_port)+'/query/' + val+'/log')

print(r3.text)

### do actual checks

if df.shape[0] == 0:
  print('Error on the output, upload a different file or check the container Score Code')
  sys.exit(1)
else:
  print('Everything should be ok!')
