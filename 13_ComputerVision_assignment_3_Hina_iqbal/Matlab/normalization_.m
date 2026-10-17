function [xyn, XYZn, T, U] = normalization_(xy, XYZ)
% Data normalization for camera calibration
% xy: 3xN matrix of image points (homogeneous coordinates)
% XYZ: 4xN matrix of world points (homogeneous coordinates)

%% Normalize image points (xy)
% Convert to inhomogeneous coordinates for normalization
xy_inh = xy(1:2,:);

% Compute mean and scale
xy_mean = mean(xy_inh, 2);
xy_centered = xy_inh - xy_mean;
scale_xy = sqrt(2) / mean(sqrt(sum(xy_centered.^2, 1)));

% Create normalization matrix T
T = [scale_xy,       0, -scale_xy*xy_mean(1);
     0,       scale_xy, -scale_xy*xy_mean(2);
     0,       0,       1];

% Normalize image points
xyn = T * xy;

%% Normalize world points (XYZ)
% Convert to inhomogeneous coordinates for normalization
XYZ_inh = XYZ(1:3,:);

% Compute mean and scale
XYZ_mean = mean(XYZ_inh, 2);
XYZ_centered = XYZ_inh - XYZ_mean;
scale_XYZ = sqrt(3) / mean(sqrt(sum(XYZ_centered.^2, 1)));

% Create normalization matrix U
U = [scale_XYZ,       0,       0, -scale_XYZ*XYZ_mean(1);
     0,       scale_XYZ,       0, -scale_XYZ*XYZ_mean(2);
     0,       0,       scale_XYZ, -scale_XYZ*XYZ_mean(3);
     0,       0,       0,       1];

% Normalize world points
XYZn = U * XYZ;
end