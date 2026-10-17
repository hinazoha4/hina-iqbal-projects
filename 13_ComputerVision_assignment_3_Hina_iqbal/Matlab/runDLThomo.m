function [H] = runDLThomo(p_i, p_f)
% Using normalized data points, use DLT algorithm to compute H
% p_i and p_f should both be 3xN matrices (homogeneous coordinates)

% Check input dimensions
if size(p_i, 1) ~= 3 || size(p_f, 1) ~= 3
    error('Input points must be in homogeneous coordinates (3xN matrices)');
end

n = size(p_i, 2);
if n < 4
    error('At least 4 point correspondences are needed');
end

A = zeros(2*n, 9);

for i = 1:n
    % Ensure we're using normalized homogeneous coordinates
    x = p_f(1,i); y = p_f(2,i); w = p_f(3,i);
    u = p_i(1,i); v = p_i(2,i);
    
    A(2*i-1, :) = [x, y, w, 0, 0, 0, -u*x, -u*y, -u*w];
    A(2*i, :)   = [0, 0, 0, x, y, w, -v*x, -v*y, -v*w];
end

[~, ~, V] = svd(A);
H = reshape(V(:, end), 3, 3)';
H = H / H(3,3); % Normalize
end