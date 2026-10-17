function dispMap = computeDisparity(im1, im2, maxDisp, windowSize)
% COMPUTEDISPARITY Computes the disparity map between rectified stereo images
%   im1, im2   : rectified grayscale images (same size)
%   maxDisp    : maximum disparity to search
%   windowSize : size of matching window (odd number)
%   dispMap    : output disparity map (same size as im1)

if size(im1, 3) == 3, im1 = rgb2gray(im1); end
if size(im2, 3) == 3, im2 = rgb2gray(im2); end

im1 = double(im1);
im2 = double(im2);

[H, W] = size(im1);
halfWin = floor(windowSize / 2);
dispMap = zeros(H, W);

for y = 1 + halfWin : H - halfWin
    for x = 1 + halfWin + maxDisp : W - halfWin
        bestSSD = inf;
        bestDisp = 0;

        patch1 = im1(y-halfWin:y+halfWin, x-halfWin:x+halfWin);

        for d = 0:maxDisp
            x2 = x - d;

            if x2 - halfWin < 1
                continue;
            end

            patch2 = im2(y-halfWin:y+halfWin, x2-halfWin:x2+halfWin);

            ssd = sum((patch1 - patch2).^2, 'all');

            if ssd < bestSSD
                bestSSD = ssd;
                bestDisp = d;
            end
        end

        dispMap(y, x) = bestDisp;
    end
end
end
