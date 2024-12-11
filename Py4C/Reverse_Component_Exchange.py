#-------------------------------------------------------------------------------
# (c) Pier Giorgio Esposito, 2024
# name                    : Reverse Component Exchange
# script-type             : Python
# description             : Swap Source and Target of a Compoment Exchange
# popup                   : enableFor(org.polarsys.capella.core.data.fa.ComponentExchange)
#
#-------------------------------------------------------------------------------
# include needed for the Capella modeller API
include('workspace://Python4Capella/simplified_api/capella.py')
if False:
    from simplified_api.capella import *

include('workspace://Python4Capella/java_api/Java_API.py')
if False:
    from java_api.Java_API import *
    
# include needed for the Requirement API
include('workspace://Python4Capella/simplified_api/requirement.py')
if False:
    from simplified_api.requirement import *

import logging

# configure logging format
logFormat = '%(asctime)-15s - %(processName)s - %(message)s'
logging.basicConfig(format=logFormat, level=logging.INFO)
logging.getLogger('py4j').setLevel(logging.ERROR)

# Retrieve the Element from the current selection
selElem = CapellaPlatform.getFirstSelectedElement()
c = ComponentExchange(selElem)

modelPath = CapellaPlatform.getModelPath(c)

# change this path to execute the script on your model (here is the IFE sample). 
# comment it if you want to use the "Run configuration" instead
aird_path = '/' + modelPath

model = CapellaModel()
model.open(aird_path)

# gets the SystemEngineering and print its name
se = model.get_system_engineering()
logging.info('Model name: %s', se.get_name())

# preparing excel file export
project_name = aird_path[0:(aird_path.index("/", 1) + 1)]
project = CapellaPlatform.getProject(project_name)

# start transaction to make modifications in the model
model.start_transaction()   
try:
    logging.info(c.get_name())    
    sp = c.get_source_port()
    logging.info(sp.get_name())
    
    spj = sp.get_java_object()
    logging.info(spj)
    
    tp = c.get_target_port()
    logging.info(tp.get_name())
    
    tpj = tp.get_java_object()
    logging.info(tpj)

    cj = c.get_java_object()
    logging.info(cj)
    
    cj.setSource(tpj)
    cj.setTarget(spj)
    
except:
    # if something went wrong we rollback the transaction
    model.rollback_transaction()
    raise
else:
    # if everything is ok we commit the transaction
    model.commit_transaction()


