## Sensor-less External Force Estimation Using LSTM Neural Networks

**Sensor-less Estimation of External Force using LSTM Neural Networks** is an interdisciplinary project conducted at TU/e (Course Code: 5ARIP10) aiming to enable a mobile robot to detect and quantify human pushes without dedicated force sensors.

The system leverages a compliance–controlled motion platform that safely yields when contacted by humans in corridors or rooms, while estimating the magnitude of the push from all directions.

For a full project overview, system design, and evaluation results, see the final group report: **5ARIP10_Final_Report_Group_Hospital_Robot_Motion_Platform.pdf**.

---

## Features

- **Sensor-less force estimation** utilizing only the existing setup (current and voltage signals from BLDC motors) thereby eliminating addtional force/torque sensors.  
- **LSTM neural network** to capture temporal patterns in sensor data for accurate prediction of external force.  
- **Data generator** scripts in MATLAB for synthetic training datasets, including varied magnitudes and direction of external force.  
- **Real-time compliance control** framework integrating estimated forces into the robot’s motion controller.

---

## Prerequisites

- **Python 3.8+** — for data preprocessing and model training.  
- **PyTorch 2.x** — used for implementing and training the LSTM model.  
- **MATLAB R2021a+** — for the data generator scripts.

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Yogi-hub/Sensor-less-Estimation-of-External-Force-using-LSTM-Neural-Networks.git
   cd Sensor-less-Estimation-of-External-Force-using-LSTM-Neural-Networks
   ```
2. **Set up Python environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```  
   Requirements include `torch`, `numpy`, `pandas`, and `scikit-learn`.
3. **Verify MATLAB scripts**  
   - Open **doc/Data generator Guide.pdf** in MATLAB.  
   - Run `data_generator.m` to produce the training dataset.

---

## Usage

### 1. Generate Training Data  
```matlab
% In MATLAB command window
run('data_generator.m');
```
This script simulates pushes of varying magnitudes and directions, exporting `.csv` files for model training.

### 2. Train LSTM Model  
```bash
python train_lstm.py --data_dir data/ --epochs 100
```
The LSTM architecture stacks two layers with dropout using PyTorch’s `torch.nn.LSTM` API.

### 3. Evaluate & Predict  
```bash
python evaluate.py --model_path checkpoints/model.pt --test_data data/test.csv
```
This outputs predicted force values and comparison plots against ground truth.

---

## Project Structure

```
├── doc/
│   ├── LSTM Guide.pdf              # Details of network architecture
│   └── Data generator Guide.pdf    # Instructions for MATLAB data generation
├── data/                           # Generated training and test datasets
├── lstm_model/                     # Python scripts for defining and training LSTM
│   ├── train_lstm.py
│   ├── evaluate.py
│   └── model.py
├── figures/                        # Plots of training curves and prediction results
├── 5ARIP10_Final_Report_Group_Hospital_Robot_Motion_Platform.pdf
└── README.md
```

---


## Contributing

We welcome improvements! Please fork the repo, make your changes, and submit a pull request. For bug reports or feature requests, open an issue on GitHub.

---




