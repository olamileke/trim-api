### Trim-Be
----
REST API backend of the Trim application written in Flask-Restful. View the live application [here](https://trimm.xyz "here").

The front end is written in Angular and can be found [here](https://github.com/olamileke/trim-fe "here").

To run this application locally, you need to have python3+ on your system. Get it 
[here](https://https://www.python.org/downloads/ "here"). Make sure to add python.exe to your operating system path variables to be able to run python scripts from the command line.

Navigate into a directory of choice on your system and run
``` 
git clone -b clone --single-branch https://github.com/olamileke/trim-be.git
```
This will clone the clone(sorry, double entendre!) branch onto your system. The clone branch contains the scrubbed configuration.py file into which you will enter relevant application secrets.

Navigate into the application root by running
```
cd Trim-be
```

At this point, we need to create the virtual machine in which the application will run. Depending on if you are working in a windows or linux environment, follow the instructions found [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/ "here") to create the virtual environment.

Activate the virtual environment by running 
```
venv\scripts\activate
```
or 
```
source venv/scripts/activate
```
for windows and linux respectively.  Now, with the virtual environment active, run the following command
```
pip install -r requirements.txt
```
This will install all the application dependences as outlined in the requirements.txt file in the app root.

