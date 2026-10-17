function [K, R, t, Kd, error] = runGoldRadialcal(xy, XYZ, Dec_type)
% Normalize data points
[xy_normalized, XYZ_normalized, T, U] = normalization_(xy, XYZ);

% Compute DLT
[Pn] = dlt(xy_normalized, XYZ_normalized);

% Distortion Coefficient Initial Values
Kd = [0 0];

% Minimize geometric error
pn = [Pn(1,:) Pn(2,:) Pn(3,:) Kd];
for i = 1:20
    pn = fminsearch(@fminGoldRadial, pn, [], xy_normalized, XYZ_normalized);
end

% Extract P and distortion coefficients
Pn = reshape(pn(1:12), 3, 4);
Kd = pn(13:14);

% Denormalize camera matrix
P = T \ Pn * U;

% Factorize camera matrix into K, R and t
if strcmp(Dec_type, 'QR')
    [K, R, C] = decomposeQR(P);
else
    [K, R, C] = decomposeEXP(P);
end

% Compute translation t = -RC
t = -R * C;

% Compute reprojection error with distortion
n = size(xy, 2);
error = 0;
cx = K(1,3); cy = K(2,3);

for i = 1:n
    % Project 3D point
    proj = P * XYZ(:, i);
    proj = proj / proj(3);
    
    % Apply radial distortion
    x = proj(1) - cx;
    y = proj(2) - cy;
    r2 = x^2 + y^2;
    L = 1 + Kd(1)*r2 + Kd(2)*r2^2;
    
    xd = cx + L*x;
    yd = cy + L*y;
    
    % Compute error
    diff = xy(1:2, i) - [xd; yd];
    error = error + sum(diff.^2);
end
error = error / n; % Average error
end