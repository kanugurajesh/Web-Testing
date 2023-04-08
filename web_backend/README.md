# Backend for Web testing

The web_backend folder contains all the files used to create backend for the web testing application.This project is developed in linux os.

# Prerequisites

1.docker  
2.python(3.8)  
3.Chrome Browser

# Project Setup  

1.run the <code>docker-compose</code> file by running the command <code>docker-compose up</code>  
2.create a python environment by running the command <code>python3 -m venv venv</code>  
3.activate the python environment by running the command <code>source venv/bin/activate</code>  
4.Install all the python modules required by the project using the command <code>pip3 install -r requirements.txt</code>  
5.chromedriver is included in the files if you are having any issues install the chromedriver according to your browser version

# Usage Instructions  

1.run the elasticsearch with the command <code>docker start elasticsearch</code>  
2.run the kibana with the command <code>docker start kibana</code>  
3.run the python file <code>tester.py</code> which performs the testing on the lambdatest website 100 times and retrieves the network logs generated when clicked on the header links <code>python3 tester.py</code> it stores about 50 network logs in a single file and stores all the files in a <code>network_logs directory.</code>  
4.run the python <code>file key_value_extraction_all.py</code> which convertes the extracted network logs into simplified version to index them into elasticsearh.All of this simpliefied network logs are stored in <code>network_log folder</code>.  
5.run the python file <code>schema_generator.py</code> which generates a schema which shows what are the fields and field type included in the network logs by running the command <code>python3 schema_generator.py</code> it creates a schema file with the name <code>schema.json</code>.  
6.run the python file <code>key_value_extraction_all_epoch.py</code> it adds some fields to the network logs if the miss any by comparing it to the <code>schema.json</code> so that it avoids any inequiality and this added fileds are given null,-1, values.run the python file with command <code>python3 key_value_extraction_epoch.py</code> all this files are stored in <code>network_logs_elasticsearch</code> directory.  
7.Then run the file <code>cluster_data_adder.py</code> which indexes the network logs to the elasticsearch cluster it creates a cluster named final_cluster and indexes the data to the cluster.The process will take time wait patiently till the process completes.  
8.When the process is completed run the runner.py file which is the api run the runner.py with the command <code>uvicorn runner:app --reload</code>.  
Make sure to install the elasticsearch api with the version specified in requirements.txt in the machine other than the environment becuase the api requires uses the elasticsearch api in the local machine.  

# Instructions  

1.Installing the <code>elasticsearch 7.10.0</code> version in the local machine can cause errors sometimes if it fails run it multiple times.It will work out.To check whether the elasticsearch 7.10.0 is installed or not you can run <code>pip3 show elasticsearch</code> if shows up information specifying elasticsearch and version 7.10.0 it means elasticsearch is installed in you local machine.  
2.To see the status,health,data stored in the cluster you can access kibana by using you browser you can go the location http://localhost:5601/  
3.click on the 3 bar icon or menu then scroll down to find management section you can find stack management click on it then click on index management in the left side  
4.Then you can see a box in the right side of the window containing the name of the cluster,health,status and all the details regarding it  
5.you can send request to the elasticsearch by using the address http://localhost:9200/  
6.Follow the all the steps correctly to make the project work.The file <code>tester.py</code> takes on average of about 350 seconds to complete its task and same with <code>cluster_data_adder.py</code>  
7.The cluster is persistent and by default it stores the data in <code>/usr/share/elasticsearch/data</code> directory make sure the usr directory have enought space to  store the data or else elasticsearch will give exceeded water mark error.  
8.You can change the number of tests you run by changing the count parameter in <code>tester.py</code> file.
