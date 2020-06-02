import sasctl
from sasctl import register_model, publish_model, Session
from sasctl.services import model_repository ## this is the important part
import pandas as pd
from pathlib import Path
import pzmm

host = 'localhost'
#host='pdcesx01077.exnet.sas.com'

publishdestination = 'localhost'

modelname = 'R_auto_docker'

project_name = 'hmeq_os'

algo = 'logistic'

s = Session(host, 'sasdemo', 'Orion123', verify_ssl = False)


### reading data form column names
data = pd.read_csv('./data/hmeq_score.csv', nrows = 5)


inputData = pd.read_csv(('./data/hmeq_score.csv'))
                        
### list inputs and outputs
inputs = data[0:3].drop(['BAD'], axis=1)
# Need one example of each var for guessing type
### can't have NaN
inputs['DEBTINC'] = .5 

outputs = data.columns.to_list()[0]
outputs = pd.DataFrame(columns=[outputs, 'P_BAD0', 'P_BAD1'])

outputs.loc[len(outputs)] = [1, 0.5, 0.5]
path = Path.cwd()

####
#### Creating input & output files
JSONFiles = pzmm.JSONFiles()

### write inputVar.json
JSONFiles.writeVarJSON(inputs, isInput=True, jPath=path)

### write outputVar.json
JSONFiles.writeVarJSON(outputs, isInput=False, jPath=path)

### Creating 
### don't use this in the real world
model_repository.delete_model('R_auto_docker')

model_repository.create_model(model = modelname,
                             project = project_name,
                             description = 'My Jenkings automatized',
                             modeler = 'Hellas',
                             algorithm = algo,
                             tool = 'R',
                             score_code_type='R',
                             function='Classification',
                             is_champion=False,
                             is_challenger=True,
                             event_prob_variable ='P_BAD1')


#### basic files

filenames = {'file':['inputVar.json','outputVar.json','scoreCode.R',
                      'model_training.R','rlogistic.rda', 'model.pmml'],
            'role':['input','output', 'score', 'train', 'resource', 'PMML']}
            
#### uploading files

for i in range(len(filenames['file'])):

    with open(path / filenames['file'][i], "rb") as _file:

        model_repository.add_model_content(
                      model = modelname, 
                      file = _file, 
                      name = filenames['file'][i], 
                      role= filenames['role'][i])
        
        print('uploaded ' + filenames['file'][i] + ' as ' + filenames['role'][i])
        _file.close()

#### Publish model

publish_model(modelname, publishdestination)