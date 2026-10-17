% Exercise 3 - Camera Calibration
close all;
clear all;
clc;

% Load calibration image
try
    IMG_NAME = 'images/image001.jpg';
    img = imread(IMG_NAME);
catch
    error('Could not load calibration image. Check file path.');
end

% Decomposition Approach (QR or EXP)
D_type = 'QR'; % Change to 'EXP' for explicit decomposition

% Get calibration points
[xy, XYZ] = getpoints(img);

% === Task 2: DLT algorithm ===
disp('=== Running DLT Calibration ===');
[K, R, t, error] = runDLTcal(xy, XYZ, D_type);
disp(K);

% === Task 3: Gold Standard algorithm ===
disp('=== Running Gold Standard Calibration ===');
[K_gold, R_gold, t_gold, error_gold] = runGoldcal(xy, XYZ, D_type);
disp(K_gold);

% === Task 4: Gold Standard with Radial Distortion ===
disp('=== Running Gold Standard with Radial Distortion ===');
[K_rad, R_rad, t_rad, Kd, error_rad] = runGoldRadialcal(xy, XYZ, D_type);
disp(K_rad);


