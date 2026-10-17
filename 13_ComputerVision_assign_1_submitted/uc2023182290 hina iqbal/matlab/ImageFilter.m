function [img1] = ImageFilter(img0, h)
    [rows, cols] = size(img0);
    [kRows, kCols] = size(h);
    
    % Padding the image with nearest-neighbor padding
    padSize = floor([kRows, kCols] / 2); % Calculate padding size based on kernel size
    img0Padded = padarray(img0, padSize, 'replicate', 'both');
    
    % Create an empty matrix for the output image
    img1 = zeros(rows, cols);
    
    % Convolution (Using sliding window)
    for i = 1:rows
        for j = 1:cols
            % Extract the sub-matrix for the current position
            subMat = img0Padded(i:i+kRows-1, j:j+kCols-1);
            % Perform element-wise multiplication and sum to get the convolved value
            img1(i, j) = sum(sum(subMat .* h));
        end
    end
end
