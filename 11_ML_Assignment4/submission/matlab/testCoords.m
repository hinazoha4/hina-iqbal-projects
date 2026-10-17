% testCoords.m
% Complete pipeline for sparse 3D reconstruction using coords.mat
% and saving extrinsic parameters for dense reconstruction

clear; clc;

im1 = imread('../data/im1.png');
im2 = imread('../data/im2.png');

load('../data/correspondences.mat');   
load('../data/intrinsics.mat');       
          

F = computeF(pts1, pts2);

load('../data/coords.mat');  
pts2 = findEpipolarMatches(im1, im2, F, pts1);

E = computeE(F, K1, K2);  

P1 = K1 * [eye(3), zeros(3,1)];  
M2s = camera2(E);                

best_count = 0;
best_pts3d = [];
best_M2 = [];
best_P2 = [];

for i = 1:4
    M2 = M2s(:,:,i);
    P2 = K2 * M2;

    pts3d = triangulation3D(P1, pts1, P2, pts2);

    homog_pts3d = [pts3d, ones(size(pts3d,1), 1)]';
    depth1 = P1(3,:) * homog_pts3d;
    depth2 = P2(3,:) * homog_pts3d;

    count = sum(depth1 > 0 & depth2 > 0);

    if count > best_count
        best_count = count;
        best_pts3d = pts3d;
        best_M2 = M2;
        best_P2 = P2;
    end
end

fprintf('Best solution has %d points in front of both cameras.\n', best_count);

figure;
scatter3(best_pts3d(:,1), best_pts3d(:,2), best_pts3d(:,3), 15, 'filled');
xlabel('X'); ylabel('Y'); zlabel('Z');
title('Sparse 3D Reconstruction from coords.mat');
axis equal; grid on;

R1 = eye(3);              
t1 = zeros(3,1);          
R2 = best_M2(:, 1:3);     
t2 = best_M2(:, 4);       

save('../data/extrinsics.mat', 'R1', 't1', 'R2', 't2');

fprintf('Saved extrinsic parameters to ../data/extrinsics.mat\n');
