function [H_F] = Homography(P_I, P_F)
% Compute homography between image and football field
% P_I: image points (2xN or 3xN)
% P_F: field points (2xN or 3xN)

% Convert to homogeneous coordinates if needed
if size(P_I, 1) == 2
    P_I = [P_I; ones(1, size(P_I, 2))];
end
if size(P_F, 1) == 2
    P_F = [P_F; ones(1, size(P_F, 2))];
end

% Verify we have enough points
if size(P_I, 2) < 4 || size(P_F, 2) < 4
    error('At least 4 point correspondences are needed');
end

% Normalize Data Points
[P_I_N, P_F_N, T_I, T_F] = normalization(P_I, P_F);

% Compute Homography
H = runDLThomo(P_I_N, P_F_N);

% Refine H using Gold Standard
H_R = RunGoldhomo(H, P_I_N, P_F_N);

% Denormalize Homography
H_F = T_I \ H_R * T_F;
H_F = H_F / H_F(3,3); % Normalize
end