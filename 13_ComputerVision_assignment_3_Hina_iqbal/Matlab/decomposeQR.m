function [K, R, C] = decomposeQR(P)
% Decompose P into K, R and t using QR decomposition
M = P(:, 1:3);

% Camera center is the right null vector of P
[~, ~, V] = svd(P);
C = V(:, end);
C = C(1:3) / C(4);

% QR decomposition of M^-1
[Q, R] = qr(inv(M));

% K is inverse of R'
K = inv(R');
K = K ./ K(3,3); % Normalize

% R is Q'
R = Q';

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