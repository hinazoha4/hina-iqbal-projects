function f = fminGold(p, xy, XYZ, w)
% Reassemble P
P = [p(1:4); p(5:8); p(9:12)];

% Compute squared geometric error
n = size(xy, 2);
error = 0;

for i = 1:n
    % Project 3D point
    proj = P * XYZ(:, i);
    proj = proj / proj(3);
    
    % Compute error
    diff = xy(1:2, i) - proj(1:2);
    error = error + sum(diff.^2);
end

% Compute cost function value
f = error;
end