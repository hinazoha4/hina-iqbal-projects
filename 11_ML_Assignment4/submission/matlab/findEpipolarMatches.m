function pts2 = findEpipolarMatches(im1, im2, F, pts1)
% FINDEPIPOLARMATCHES - Robust matching using Gaussian-weighted NCC
%   Input:
%       im1, im2 - Grayscale or RGB images
%       F        - Fundamental matrix (3x3)
%       pts1     - Nx2 matrix of points in image 1
%   Output:
%       pts2     - Nx2 matrix of matched points in image 2

if size(im1, 3) == 3, im1 = rgb2gray(im1); end
if size(im2, 3) == 3, im2 = rgb2gray(im2); end

[h1, w1] = size(im1);
[h2, w2] = size(im2);
win = 7; % Half patch size (patch is 15x15)
pts2 = nan(size(pts1));

gauss = fspecial('gaussian', 2*win+1, 1.5);

for i = 1:size(pts1, 1)
    x1 = round(pts1(i,1));
    y1 = round(pts1(i,2));

    % Skip if patch would go out of bounds in im1
    if x1 - win < 1 || x1 + win > w1 || y1 - win < 1 || y1 + win > h1
        continue;
    end

    x1 = round(pts1(i,1));
    y1 = round(pts1(i,2));
    tpl = double(im1(y1-win:y1+win, x1-win:x1+win));
    tpl_mean = sum(tpl(:) .* gauss(:));
    tpl_std  = sqrt(sum((tpl(:) - tpl_mean).^2 .* gauss(:))) + eps;
    tpl_z = (tpl(:) - tpl_mean) .* sqrt(gauss(:));

    l = F * [x1; y1; 1];
    l = l / norm(l(1:2));

    if abs(l(2)) > abs(l(1))
        y = linspace(1, h2, 200);
        x = round((-l(2) * y - l(3)) / l(1));
    else
        x = linspace(1, w2, 200);
        y = round((-l(1) * x - l(3)) / l(2));
    end

    valid = x - win >= 1 & x + win <= w2 & ...
            y - win >= 1 & y + win <= h2;
    x = x(valid);
    y = y(valid);

    best_ncc = -Inf;
    best_match = [NaN, NaN];

    for j = 1:length(x)
        x2 = x(j);
        y2 = y(j);
        x2 = round(x2);
        y2 = round(y2);
        patch = double(im2(y2-win:y2+win, x2-win:x2+win));
        patch_mean = sum(patch(:) .* gauss(:));
        patch_std  = sqrt(sum((patch(:) - patch_mean).^2 .* gauss(:))) + eps;
        patch_z = (patch(:) - patch_mean) .* sqrt(gauss(:));

        ncc = sum(tpl_z .* patch_z) / (tpl_std * patch_std);

        if ncc > best_ncc
            best_ncc = ncc;
            best_match = [x2, y2];
        end
    end

    pts2(i, :) = best_match;
end
end
