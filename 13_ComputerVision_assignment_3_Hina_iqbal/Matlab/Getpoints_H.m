function [xy1, xy2] = Getpoints_H(img1, img2)
% GETPOINTS Get corresponding points from two images for homography estimation
% Returns:
%   xy1 - 3xN matrix of homogeneous coordinates from first image
%   xy2 - 3xN matrix of homogeneous coordinates from second image

xy1 = [];
xy2 = [];
n = 0;

% Show first image and collect points
figure;
imshow(img1);
title('Click points on first image (right click to finish)');

but = 1;
while but == 1
    [xi, yi, but] = ginput(1);
    if but ~= 1, break; end
    hold on;
    plot(xi, yi, 'ro', 'MarkerSize', 10, 'LineWidth', 2);
    text(xi+10, yi+10, num2str(n+1), 'Color', 'r', 'FontSize', 12);
    hold off;
    n = n + 1;
    xy1(:, n) = [xi; yi; 1]; % Store in homogeneous coordinates
end

% Show second image and collect corresponding points
figure;
imshow(img2);
title(sprintf('Click %d corresponding points on second image', n));

for i = 1:n
    [xi, yi] = ginput(1);
    hold on;
    plot(xi, yi, 'ro', 'MarkerSize', 10, 'LineWidth', 2);
    text(xi+10, yi+10, num2str(i), 'Color', 'r', 'FontSize', 12);
    hold off;
    xy2(:, i) = [xi; yi; 1]; % Store in homogeneous coordinates
end

% Verify we got the same number of points in both images
if size(xy1, 2) ~= size(xy2, 2)
    error('Number of points in both images must match');
end
end