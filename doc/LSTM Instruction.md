# LSTM Training Guide
In this Guide, installation guides for training LSTM model are documented.

## Pre-requisites

* Make sure you have Python installed. [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) is recommended. 
### Python packages
To train LSTM model using Pytorch, some packages are required. 
* Pytorch
  * Please follow the instruction from: https://pytorch.org/get-started/locally/.
    * Note: CUDA Toolkie is also required: https://developer.nvidia.com/cuda-zone.
  * It is recommend to use GPU version.
* numpy
* tqdm
* matplotlib
* scipy

## Training processing

### Step 1: Prepare data

The data consists of the results of simulation. These results should be stored in `'/AI model/data/raw_data'`. And they should be named as `current_<i>`, `voltage_<i>` and `External_Force_<i>`, of which `<i>` means the i-th simulaion.

### Step 2: Run matlab script
`/AI model/data/adataprocessing.m` will transform the simulation results in `/AI model/data/raw_data/` into `/AI model/data/raw_dataset.mat`, which will be used in later training procedure.

Open the `/AI model/data/adataprocessing.m` and run.

### Step 3: Run jupyter notebook

1. Open the '/AI model/LSTM.ipynb' and select the suitable python environment
2. Change the configuration in `1.1 Data parameters` and `2.2 Model parameters` if needed.
   1. Normally, only `model_name` should be changed.
3. Run the notebook.
4. The results will be stored in `./models/<model_name>`
   1. `/epochs` stores all models of each epoch.
   2. `/results` stores training loss and validation loss. The `test_output.pt` and `test_targe/pt` are target values in test set and corresponding model predictions. The `mse_rmse.pt` is the MSE and RMSE on test set. `loss.png` and `test.png` are figures showing the loss w.r.t. epoch and the prediction of the model on test set respectively.
   3. `/running_vars` stores the splited training set, validation set and test set.

