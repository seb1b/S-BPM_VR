# S-PBM_VR

This is a project in the proceedings of the Virtual Engineering Practical at the 
Institute for Information Management in Engineering @ Karlsruhe Institute of Technology KIT




GETTING STARTED__GROUP2_HARDWARE_SETUP

--KINECT:
Follow instruction:
http://www.cs.princeton.edu/~edwardz/tutorials/kinect2/kinect0.html

https://mva.microsoft.com/en-us/training-courses/programming-kinect-for-windows-v2-jump-start-9088?l=Ju7xHKf4_6604984382
Extract hand points from sceleton.

--PROTOCOLL_FOR_SENDING_MESSAGES:
follow tutorial instruction:
https://www.rabbitmq.com/tutorials/tutorial-one-dotnet.html

can be done on windows side with C# or Python and then on Linux side with Python

--MYO:

using PyoConnect_v2.0 written by  Fernando Cosentino - http://www.fernandocosentino.net/pyoconnect
For writing a  new application, put your python script in
S-BPM_VR/HardwareInterface/Linux/Myo/scripts

In a terminal, navigate to the Myo folder and use python to run PyoManager.pyc:
$ python PyoManager.pyc

The "Connect Myo" and "Disconnect" buttons allow you to connect to your armband.

For each script found in the Scripts folder, there will be a line in the menu, with a button to enable/disable that particular script, just like MyoConnect for windows. More than one script can be active at the same time. In fact, all scripts can be active at the same time.



