function [K, R, t, error] = runDLTcal(xy, XYZ, Decomp)
% Normalize data points
[xy_normalized, XYZ_normalized, T, U] = normalization_(xy, XYZ);

% Compute DLT
[P_normalized] = dlt(xy_normalized, XYZ_normalized);

% Denormalize camera matrix
P = T \ P_normalized * U;

% Factorize camera matrix into K, R and t
if strcmp(Decomp, 'QR')
    [K, R, C] = decomposeQR(P);
else
    [K, R, C] = decomposeEXP(P);
end

% Compute translation t = -RC
t = -R * C;

% Compute reprojection error
n = size(xy, 2);
error = 0;
for i = 1:n
    proj = P * XYZ(:, i);
    proj = proj / proj(3);
    diff = xy(1:2, i) - proj(1:2);
    error = error + sum(diff.^2);
end
error = error / n; % Average error
end