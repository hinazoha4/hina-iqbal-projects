function [H_R] = RunGoldhomo(H, p_i, p_f)
% Refines the estimation of H using nonlinear optimization (Gold Standard)
options = optimset('Display', 'off', 'MaxIter', 1000);
h = reshape(H', 9, 1);
h = fminsearch(@(x) homography_error(x, p_i, p_f), h, options);
H_R = reshape(h, 3, 3)';
end

function error = homography_error(h, p_i, p_f)
% Compute error for homography refinement
H = reshape(h, 3, 3)';
n = size(p_i, 2);
error = 0;

for i = 1:n
    proj = H * p_f(:, i);
    proj = proj / proj(3);
    diff = p_i(1:2, i) - proj(1:2);
    error = error + sum(diff.^2);
end
end