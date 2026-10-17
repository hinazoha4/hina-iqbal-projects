%% 3D Camera and Calibration Pattern Visualization


clear all; close all; clc;

%% Load calibration data
img_calib = imread('images/image001.jpg');
[xy, XYZ] = getpoints(img_calib); % Get calibration points

%% Run calibration to get camera position (using QR decomposition)
D_type = 'QR';
[K, R, t, ~] = runDLTcal(xy, XYZ, D_type);

%% 3D Visualization
figure('Name','3D Camera and Calibration Pattern','Position',[100 100 800 600]);
hold on; axis equal; grid on; view(3);
title('3D Camera Position Relative to Calibration Pattern');

% Plot calibration pattern points
scatter3(XYZ(1,:), XYZ(2,:), XYZ(3,:), 50, 'filled', 'MarkerFaceColor', [0.8 0.2 0.2]);
text(XYZ(1,:), XYZ(2,:), XYZ(3,:), num2str((1:size(XYZ,2))'), ...
    'Color', 'red', 'FontSize', 8, 'HorizontalAlignment','center');

% Plot camera coordinate system
cam_center = -R' * t;
cam_axis_length = 0.5 * max(range(XYZ(1:3,:)')); % Scale based on pattern size

% Camera axes (RGB = XYZ)
quiver3(cam_center(1), cam_center(2), cam_center(3), ...
        cam_axis_length*R(1,1), cam_axis_length*R(2,1), cam_axis_length*R(3,1), ...
        'r', 'LineWidth', 2, 'MaxHeadSize', 0.5); % X-axis (red)
quiver3(cam_center(1), cam_center(2), cam_center(3), ...
        cam_axis_length*R(1,2), cam_axis_length*R(2,2), cam_axis_length*R(3,2), ...
        'g', 'LineWidth', 2, 'MaxHeadSize', 0.5); % Y-axis (green)
quiver3(cam_center(1), cam_center(2), cam_center(3), ...
        cam_axis_length*R(1,3), cam_axis_length*R(2,3), cam_axis_length*R(3,3), ...
        'b', 'LineWidth', 2, 'MaxHeadSize', 0.5); % Z-axis (blue)

% Camera frustum representation
frustum_depth = 0.3 * max(range(XYZ(1:3,:)'));
frustum_points = [
    0 0 0;
    frustum_depth frustum_depth frustum_depth;
    0 0 0;
    -frustum_depth frustum_depth frustum_depth;
    0 0 0;
    frustum_depth -frustum_depth frustum_depth;
    0 0 0;
    -frustum_depth -frustum_depth frustum_depth]';

% Transform frustum points to world coordinates
frustum_world = R' * (frustum_points - t);

% Plot frustum lines
plot3([cam_center(1) frustum_world(1,2)], ...
      [cam_center(2) frustum_world(2,2)], ...
      [cam_center(3) frustum_world(3,2)], 'k-', 'LineWidth', 1);
plot3([cam_center(1) frustum_world(1,4)], ...
      [cam_center(2) frustum_world(2,4)], ...
      [cam_center(3) frustum_world(3,4)], 'k-', 'LineWidth', 1);
plot3([cam_center(1) frustum_world(1,6)], ...
      [cam_center(2) frustum_world(2,6)], ...
      [cam_center(3) frustum_world(3,6)], 'k-', 'LineWidth', 1);
plot3([cam_center(1) frustum_world(1,8)], ...
      [cam_center(2) frustum_world(2,8)], ...
      [cam_center(3) frustum_world(3,8)], 'k-', 'LineWidth', 1);

% Add labels and legend
xlabel('X (m)'); ylabel('Y (m)'); zlabel('Z (m)');
legend('Calibration Points', 'X-axis', 'Y-axis', 'Z-axis', 'Frustum');
text(cam_center(1), cam_center(2), cam_center(3), ' Camera', ...
    'Color','blue','FontSize',10, 'VerticalAlignment','bottom');

% Set nice viewing angle
view(30, 30);
rotate3d on; % Enable interactive rotation