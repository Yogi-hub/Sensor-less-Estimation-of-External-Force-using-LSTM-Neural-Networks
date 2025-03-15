## Data generation using Simulink

Data is required to train, validate and test the LSTM model. As the real robot nor any pre-built simulation environments are available to acquire the data, it is generated using the Simulink models. Data is to be generated for [six cases](https://tuenl-my.sharepoint.com/:i:/g/personal/y_dhanabal_student_tue_nl/ERWtA0D3HN5HpTCXQH8e-zUBPt4_9_1A0rlMA7W25U9ZVw?e=LVYdXC), as mentioned in report. 

Separate set of files were used for data generation. The table below lists out the files used for respective cases.

| Case |  Simulink model  | Multiple simulation setup file |
|:-----:|:--------:|:------:|
| 1   |     Case_1.slx     | Case_1.mldatx |
| 2   |     Case_2.slx     | Case_2.mldatx |
| 3   |     Case_3.slx     | Case_3.mldatx |
| 4   |     Case_4.slx     | Case_4.mldatx |
| 5   |     Case_5.slx     | Case_5.mldatx |
| 6   |     Case_6.slx     | Case_6.mldatx |

Following are the Simulink add-ons which must be installed before running the simulation: Simscape Electrical, Simulink Control Design, Simulink and Simscape. Both the Simulink model file and Multiple simulation setup file must be located in the same folder. The range of values (for initial speed and external force) can be set in Multiple simulation setup file.

To get an overview about multiple simulations setup using Simulink, please refer this [ page](https://nl.mathworks.com/help/simulink/slref/multiplesimulations.html). Using the panel, a design study can be created, where required block parameter(s) for which value is to be changes across simulations can be selected. By this way, the same simulation can be executed multiple times for different values of chosen block parameters. In this project, the initial speed, the final speed (only for case 3 to 6) and external force are considered as block parameters.

The generated data is stored as MAT-files to the path specified in the 'To File' block, present inside the visualization block.
