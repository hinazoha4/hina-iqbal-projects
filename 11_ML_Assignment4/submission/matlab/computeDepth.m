function depthMap = computeDepth(dispMap, K1, K2, R1, R2, t1, t2, bits)
% COMPUTEDEPTH - Computes depth map from disparity map and camera parameters
%   Inputs:
%     dispMap - Disparity map (double matrix)
%     K1, K2  - Intrinsic matrices
%     R1, R2  - Rotation matrices
%     t1, t2  - Translation vectors
%     bits    - Number of bits for disparity representation (e.g., 16, 8, 6, 4)
%   Output:
%     depthMap - Depth map (same size as disparity map)

f = K1(1,1);  

C1 = -R1' * t1;
C2 = -R2' * t2;
b = norm(C2 - C1);  

max_disp_val = 2^bits - 1;
dispMap_quantized = round(dispMap / max(dispMap(:)) * max_disp_val);
dispMap_scaled = double(dispMap_quantized) / max_disp_val * max(dispMap(:));

depthMap = zeros(size(dispMap));
valid = dispMap_scaled > 0;
depthMap(valid) = (b * f) ./ dispMap_scaled(valid);
depthMap(~valid) = 0;  

end
