clc;clear;
load('../data/correspondences.mat'); 

I1 = imread('../data/im1.png');
I2 = imread('../data/im2.png');

F = computeF(pts1, pts2);

displayEpipolar(I1, I2, F);