clear; clc;

im1 = imread('../data/im1.png');  
im2 = imread('../data/im2.png');  

maxDisp = 20;        
windowSize = 3;      

disp('Computing disparity map...');
dispMap = computeDisparity(im1, im2, maxDisp, windowSize);

dispMap_vis = dispMap / maxDisp;  

figure;
imshow(dispMap_vis, []);
colormap jet; colorbar;
title(sprintf('Disparity Map (Window = %d, Max Disp = %d)', windowSize, maxDisp));
