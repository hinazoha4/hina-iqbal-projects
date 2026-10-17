function [Img_O] = image_undistort(Img_I, K, R, t, Kd)
% Remove distortion from Img_I using camera parameters and distortion coefficients
k1 = Kd(1);
k2 = Kd(2);

% Get image size
[rows, cols, ~] = size(Img_I);
Img_O = uint8(zeros(size(Img_I)));

% Principal point
cx = K(1,3);
cy = K(2,3);

% Inverse mapping (undistorted to distorted)
for y = 1:rows
    for x = 1:cols
        % Convert to normalized coordinates
        xn = (x - cx) / K(1,1);
        yn = (y - cy) / K(2,2);
        
        % Apply radial distortion
        r2 = xn^2 + yn^2;
        L = 1 + k1*r2 + k2*r2^2;
        
        xd = cx + L*xn*K(1,1);
        yd = cy + L*yn*K(2,2);
        
        % Bilinear interpolation
        xd_floor = floor(xd);
        yd_floor = floor(yd);
        xd_ceil = min(ceil(xd), cols);
        yd_ceil = min(ceil(yd), rows);
        
        if xd_floor >= 1 && xd_ceil <= cols && yd_floor >= 1 && yd_ceil <= rows
            % Get surrounding pixels
            a = xd - xd_floor;
            b = yd - yd_floor;
            
            pixel = (1-a)*(1-b)*double(Img_I(yd_floor, xd_floor, :)) + ...
                    a*(1-b)*double(Img_I(yd_floor, xd_ceil, :)) + ...
                    (1-a)*b*double(Img_I(yd_ceil, xd_floor, :)) + ...
                    a*b*double(Img_I(yd_ceil, xd_ceil, :));
                
            Img_O(y, x, :) = uint8(pixel);
        end
    end
end
end