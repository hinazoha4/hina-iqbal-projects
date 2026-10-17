function [K, R, C] = decomposeEXP(P)
% Decompose P into K, R and t using explicit decomposition
M = P(:, 1:3);

% Camera center is the right null vector of P
[~, ~, V] = svd(P);
C = V(:, end);
C = C(1:3) / C(4);

% Compute intrinsic and rotation matrices
a1 = M(1, 1:3)';
a2 = M(2, 1:3)';
a3 = M(3, 1:3)';

% Compute rho and r3
rho = 1 / norm(a3);
r3 = rho * a3;

% Compute u0 and v0
u0 = rho^2 * (a1' * a3);
v0 = rho^2 * (a2' * a3);

% Compute theta
cross13 = cross(a1, a3);
cross23 = cross(a2, a3);
theta = acos(-(cross13' * cross23) / (norm(cross13) * norm(cross23)));

% Compute alpha and beta
sin_theta = sin(theta);
alpha = rho^2 * norm(cross13) * sin_theta;
beta = rho^2 * norm(cross23) * sin_theta;

% Compute r1 and r2
r1 = (rho^2 * sin_theta / beta) * cross23;
r2 = cross(r3, r1);

% Form K and R
K = [alpha, -alpha*cot(theta), u0;
     0, beta/sin(theta), v0;
     0, 0, 1];
R = [r1'; r2'; r3'];

% Ensure positive diagonal for K
if K(1,1) < 0
    K(:,1) = -K(:,1);
    R(1,:) = -R(1,:);
end
if K(2,2) < 0
    K(:,2) = -K(:,2);
    R(2,:) = -R(2,:);
end
if K(3,3) < 0
    K(:,3) = -K(:,3);
    R(3,:) = -R(3,:);
end
end