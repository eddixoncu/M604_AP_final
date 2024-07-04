# Vehicle Verification System 
The his a web application that help to transportation authority to verify  if it is feasible change the ownership of a vehicles.
If the vehicle doesn't have any pending infraction to be paid, the application allows the user to change the owner of a vehicle. 

#Getting Started

# Installing
you must fist clone the repository in to your local machine:
git clone https://github.com/eddixoncu/M604_AP_final.git


# Prerequisites
This project was implemented with python programing language, with flask and its extension Flask WTF.
It is recommended the using of virtual enviroments

In windows the comand is : 

in powershell locate the root folder and then type:
 python -m venv env
<p align="center">
  <img src="img_md\01.png">
</p>
Then write.\env\Scripts\activate
<p align="center">
  <img src="img_md\02.png">
</p>

For Mac and Linux systems the instructions are similar, except to activate should type env/bin/activate.

To install the dependencies, use the pip utility:
pip install -r .\dependencies.txt
<p align="center">
  <img src="img_md\03.png">
</p>

# Application
To run the application the following command should be executed:

flask run 

<p align="center">
  <img src="img_md\04.png">
</p>

Then open a browser and go to http://127.0.0.1:5000/

<p align="center">
  <img src="img_md\05.png">
</p>



