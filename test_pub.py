import docker
import socket
from contextlib import closing

### defining function to find free port
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

### model and host options
modelname = 'r_auto_docker'

client = docker.DockerClient(base_url='tcp://localhost:2375')

# img_list = client.images.list()
# img_list

# image = client.images.list(filters={'reference':'127.0.0.1:5000/'+modelname})

## Find a free port

free_port = find_free_port()

### delete old container of same same
old_con = client.containers.get(modelname)
old_con.stop()
old_con.remove()

#### Run the container
### here you can setup container limitations
### such as CPU usage

container = client.containers.run('127.0.0.1:5000/'+modelname,
                                      detach=True,
                                 ports = {'8080/tcp':str(free_port)},
                                 name = modelname)
container.logs()

### container info

container.attrs['Config']


#### container model folders
exit_code, output = container.exec_run("ls",
                                      workdir = '/pybox/model')

print(output.decode("utf-8"))

### There is a bug, MM has a standard _score.R file that must be
### substituted by your actual score code
### since this change is made inside the container when uploaded
### it must be changed everytime the container dies
### it's an workaround for first deployment
### not very reliable yet

exit_code, output = container.exec_run("cp scoreCode.R _score.R",
                                      workdir = '/pybox/model')

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
