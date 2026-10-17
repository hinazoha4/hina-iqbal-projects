function f = fminGoldRadial(p, xy, XYZ, w)
% Reassemble P and distortion coefficients
P = [p(1:4); p(5:8); p(9:12)];
k1 = p(13);
k2 = p(14);

% Principal point (assume it's in the middle of the image)
cx = P(1,3);
cy = P(2,3);

n = size(xy, 2);
error = 0;

for i = 1:n
    % Project 3D point
    proj = P * XYZ(:, i);
    proj = proj / proj(3);
    
    % Apply radial distortion
    x = proj(1) - cx;
    y = proj(2) - cy;
    r2 = x^2 + y^2;
    L = 1 + k1*r2 + k2*r2^2;
    
    xd = cx + L*x;
    yd = cy + L*y;
    
    % Compute error
    diff = xy(1:2, i) - [xd; yd];
    error = error + sum(diff.^2);
end

% Compute cost function value
f = error;
end