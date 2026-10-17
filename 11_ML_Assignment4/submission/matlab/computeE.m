function E = computeE(F, K1, K2)
% COMPUTEE Computes the essential matrix from the fundamental matrix
%   Input:
%       F - Fundamental matrix (3x3)
%       K1 - Intrinsic matrix for first camera (3x3)
%       K2 - Intrinsic matrix for second camera (3x3)
%   Output:
%       E - Essential matrix (3x3)

E = K2' * F * K1;

[U, S, V] = svd(E);
S(3,3) = 0;
E = U * S * V';

E = E / norm(E);
end