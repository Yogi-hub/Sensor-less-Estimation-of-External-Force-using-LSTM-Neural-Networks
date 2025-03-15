%% determine simulation config
clc
clear
close
pic_index = 5;
path = './raw_data/current_'+string(pic_index)+'.mat';
load(path)
subplot(3,1,1)
plot(i.Time,i.Data)
ylabel('current')
title("Sample "+string(pic_index))
path = './raw_data/voltage_'+string(pic_index)+'.mat';
load(path)
subplot(3,1,2)
plot(v.Time,v.Data(:,2))
ylabel('voltage')
path = './raw_data/External_Force_'+string(pic_index)+'.mat';
load(path)
subplot(3,1,3)
plot(force.Time,force.Data)
ylabel('force')
%% set parameters
clc
clear
start_index = 101; %start time
end_index = 1000; %end time
files = dir(fullfile('./raw_data/', 'current_*.mat'));
sample_num = length(files); %Maximum value of the number in the filename, i.e. current_sample_num
current_data = zeros(sample_num,end_index-start_index+1);
force_data = zeros(sample_num,end_index-start_index+1);
voltage_data = zeros(sample_num,end_index-start_index+1);

%% process data
for sample_i = 1:sample_num
    path = './raw_data/current_'+string(sample_i)+'.mat';
    load(path)
    current_raw = [i.Data];
    current_data(sample_i,:) = current_raw(start_index:end_index)';
    clear i

    path = './raw_data/voltage_'+string(sample_i)+'.mat';
    load(path)
    voltage_raw = [v.Data(:,2)];
    voltage_data(sample_i,:) = voltage_raw(start_index:end_index)';
    clear v

    path = './raw_data/External_Force_'+string(sample_i)+'.mat';
    load(path)
    force_raw = [force.Data];
    force_data(sample_i,:) = force_raw(start_index:end_index)';
    clear force
end
%% save data
save("raw_dataset.mat","force_data","voltage_data","current_data",'-mat')
%% plot a sample
plot_index = 1000;
subplot(3,1,1)
plot(current_data(plot_index,:))
ylabel('current')
title("Sample "+string(plot_index))
subplot(3,1,2)
plot(voltage_data(plot_index,:))
ylabel('voltage')
subplot(3,1,3)
plot(force_data(plot_index,:))
ylabel('force')

