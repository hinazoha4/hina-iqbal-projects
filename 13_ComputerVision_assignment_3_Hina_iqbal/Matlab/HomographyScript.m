% Exervice 3
%
close all;
clear all;

IMG_NAME = 'images/futebol.png';
img_I = imread(IMG_NAME);
image(img_I);

IMG_NAME = 'images/CampoJogo.jpg';
img_F = imread(IMG_NAME);
image(img_F);

% get corresponding landmark points between image and football field
% measures. Use mouse click to acquire pixel coordinates.
% Adapt the getpoints function for the purpose of homography estimation
[P_I, P_F]=Getpoints_H(img_I,img_F);

% Normalize data and Compute Homography 
H=Homography(P_I,P_F);
disp(H);

% Use computed Homography to extract measurements from "futebol" image.

CheckMeasures(H, img_I);


    

