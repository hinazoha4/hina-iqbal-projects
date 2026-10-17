function [descriptor] = SimpleFeatureDescriptor(img, pt)
    % Extract 5x5 patch centered at the keypoint
    x = round(pt.x);
    y = round(pt.y);
    
    % Get patch coordinates with boundary checking
    [rows, cols] = size(img);
    x_min = max(1, x-2);
    x_max = min(cols, x+2);
    y_min = max(1, y-2);
    y_max = min(rows, y+2);
    
    % Extract patch
    patch = img(y_min:y_max, x_min:x_max);
    
    % Handle boundary cases by padding with zeros
    if size(patch,1) < 5 || size(patch,2) < 5
        padded_patch = zeros(5,5);
        start_row = 3 - (y - y_min);
        start_col = 3 - (x - x_min);
        end_row = start_row + size(patch,1) - 1;
        end_col = start_col + size(patch,2) - 1;
        padded_patch(start_row:end_row, start_col:end_col) = patch;
        patch = padded_patch;
    end
    
    % Vectorize the patch to create descriptor
    descriptor = patch(:)';
end