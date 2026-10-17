function [xy, XYZ] = getpoints(img)
% GETPOINTS_CALIB Get image points and their 3D coordinates for calibration
% Input:
%   img - calibration image (checkerboard pattern)
% Outputs:
%   xy - 3xN matrix of image points in homogeneous coordinates
%   XYZ - 4xN matrix of 3D world points in homogeneous coordinates

xy = [];
XYZ = [];
n = 0;

% Display instructions
disp('=== Camera Calibration Point Collection ===');
disp('1. Click on checkerboard corners in the image');
disp('2. For each point, enter its real-world [X Y Z] coordinates');
disp('3. Right-click to finish');

% Create figure
fig = figure;
imshow(img);
title('Click on checkerboard corners (right-click to finish)');
hold on;

% Collect points
but = 1;
while but == 1
    % Get image point
    [xi, yi, but] = ginput(1);
    if but ~= 1
        break; % Exit on right click
    end
    
    % Plot the point
    plot(xi, yi, 'ro', 'MarkerSize', 10, 'LineWidth', 2);
    text(xi+10, yi+10, num2str(n+1), 'Color', 'r', 'FontSize', 12);
    
    % Store image point (homogeneous coordinates)
    n = n + 1;
    xy(:, n) = [xi; yi; 1];
    
    % Get corresponding 3D coordinates
    prompt = {sprintf('Enter [X Y Z] coordinates for point %d (in meters):', n)};
    dlgtitle = '3D Coordinates Input';
    dims = [1 35];
    definput = {'0 0 0'};
    answer = inputdlg(prompt, dlgtitle, dims, definput);
    
    % Convert input to numerical values
    XYZi = str2num(answer{1});
    if numel(XYZi) ~= 3
        warning('Invalid input. Expected 3 values. Using [0 0 0]');
        XYZi = [0 0 0];
    end
    
    % Store world point (homogeneous coordinates)
    XYZ(:, n) = [XYZi(:); 1];
end

hold off;
close(fig);

% Verify we have enough points
if n < 6
    error('Need at least 6 points for calibration (got %d)', n);
end

fprintf('Successfully collected %d calibration points\n', n);
end