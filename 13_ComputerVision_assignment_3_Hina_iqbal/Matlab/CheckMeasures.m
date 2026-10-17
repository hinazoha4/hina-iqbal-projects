function CheckMeasures(H, img)
% Using the computed homography, obtain distances and angles in the football field
figure;
imshow(img);
title('Click two points to measure distance');
hold on;

% Get two points from user
[x, y] = ginput(2);
plot(x, y, 'ro-');

% Convert to homogeneous coordinates
p1 = [x(1); y(1); 1];
p2 = [x(2); y(2); 1];

% Transform to field coordinates
field_p1 = H \ p1; field_p1 = field_p1 / field_p1(3);
field_p2 = H \ p2; field_p2 = field_p2 / field_p2(3);

% Calculate distance in field coordinates
distance = norm(field_p1(1:2) - field_p2(1:2));
fprintf('Distance between points: %.2f meters\n', distance/10);

% Optional: Add angle measurement
title(sprintf('Distance: %.2f meters', distance/10));
hold off;
end