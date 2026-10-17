function [K, R, t, error] = runGoldcal(xy, XYZ, Dec_type)
% Normalize data points
[xy_normalized, XYZ_normalized, T, U] = normalization_(xy, XYZ);

% Compute DLT
[Pn] = dlt(xy_normalized, XYZ_normalized);

% Minimize geometric error
pn = [Pn(1,:) Pn(2,:) Pn(3,:)];
for i = 1:20
    pn = fminsearch(@fminGold, pn, [], xy_normalized, XYZ_normalized);
end
Pn = reshape(pn, 3, 4);

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