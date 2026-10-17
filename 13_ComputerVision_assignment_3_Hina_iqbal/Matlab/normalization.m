function [xyn, XYZn, T, U] = normalization(xy, XYZ)
% Data normalization for homography estimation
% xy: first set of points (3xN)
% XYZ: second set of points (3xN)

% Normalize first set of points (xy)
xy_mean = mean(xy(1:2, :), 2);
xy_centered = xy(1:2, :) - xy_mean;
scale_xy = sqrt(2) / mean(sqrt(sum(xy_centered.^2, 1)));

T = [scale_xy, 0, -scale_xy*xy_mean(1);
     0, scale_xy, -scale_xy*xy_mean(2);
     0, 0, 1];
xyn = T * xy;

% Normalize second set of points (XYZ)
XYZ_mean = mean(XYZ(1:2, :), 2);
XYZ_centered = XYZ(1:2, :) - XYZ_mean;
scale_XYZ = sqrt(2) / mean(sqrt(sum(XYZ_centered.^2, 1)));

U = [scale_XYZ, 0, -scale_XYZ*XYZ_mean(1);
     0, scale_XYZ, -scale_XYZ*XYZ_mean(2);
     0, 0, 1];
XYZn = U * XYZ;
end