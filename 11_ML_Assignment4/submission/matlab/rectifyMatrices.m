function [M1, M2, K1n, K2n, R1n, R2n, t1n, t2n] = rectifyMatrices(K1, K2, R1, R2, t1, t2)
% RECTIFYMATRICES Computes rectification matrices for stereo rectification
%   Inputs:
%     K1, K2 - intrinsic matrices
%     R1, R2 - rotation matrices of left and right cameras
%     t1, t2 - translation vectors of left and right cameras
%   Outputs:
%     M1, M2 - rectification matrices
%     K1n, K2n - new intrinsic matrices (typically K2)
%     R1n, R2n - new rotation matrices for left and right
%     t1n, t2n - new translation vectors for left and right

C1 = -inv(R1) * t1;
C2 = -inv(R2) * t2;

r1 = (C2 - C1); r1 = r1 / norm(r1); 
old_z = R1(3, :)';                  
r2 = cross(old_z, r1); r2 = r2 / norm(r2); 
r3 = cross(r1, r2);                       
R_rect = [r1'; r2'; r3'];                

K_new = K2;

t1n = -R_rect * C1;
t2n = -R_rect * C2;

M1 = K_new * R_rect * inv(K1 * R1);
M2 = K_new * R_rect * inv(K2 * R2);

K1n = K_new;
K2n = K_new;
R1n = R_rect;
R2n = R_rect;

end
