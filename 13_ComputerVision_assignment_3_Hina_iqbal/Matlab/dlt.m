function [P] = dlt(xy, XYZ)
% Computes DLT, xy and XYZ should be normalized before calling this function
n = size(xy, 2);
A = zeros(2*n, 12);

for i = 1:n
    X = XYZ(1,i); Y = XYZ(2,i); Z = XYZ(3,i); W = XYZ(4,i);
    x = xy(1,i); y = xy(2,i); w = xy(3,i);
    
    A(2*i-1, :) = [X, Y, Z, W, 0, 0, 0, 0, -x*X, -x*Y, -x*Z, -x*W];
    A(2*i, :) = [0, 0, 0, 0, X, Y, Z, W, -y*X, -y*Y, -y*Z, -y*W];
end

[~, ~, V] = svd(A);
P = reshape(V(:, end), 4, 3)';
end