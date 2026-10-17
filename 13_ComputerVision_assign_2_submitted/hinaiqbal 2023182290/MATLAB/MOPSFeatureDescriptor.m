function [descriptor] = MOPSFeatureDescriptor(img, pt, N)
    % Create transformation to canonical orientation
    angle = -pt.orientation; % Negative because we want to rotate back to canonical
    
    % Create affine transformation matrix
    scale = 8/N; % Scale from NxN to 8x8
    T = [cosd(angle) -sind(angle) 0; 
         sind(angle)  cosd(angle) 0;
         0           0           1];
    
    S = [scale   0     0;
         0     scale   0;
         0       0     1];
    
    % Combine transformations
    TForm = affine2d(S * T);
    
    % Extract NxN patch centered at keypoint with boundary checks
    x = round(pt.x);
    y = round(pt.y);
    half_N = floor(N/2);
    
    % Get image size
    [rows, cols] = size(img);
    
    % Calculate patch boundaries with clamping
    x_min = max(1, x-half_N);
    x_max = min(cols, x+half_N);
    y_min = max(1, y-half_N);
    y_max = min(rows, y+half_N);
    
    % Extract patch
    patch = img(y_min:y_max, x_min:x_max);
    
    % Handle boundary cases by padding with mean value
    if size(patch,1) < N || size(patch,2) < N
        mean_val = mean(patch(:));
        padded_patch = ones(N,N) * mean_val;
        start_row = half_N + 1 - (y - y_min);
        start_col = half_N + 1 - (x - x_min);
        end_row = start_row + size(patch,1) - 1;
        end_col = start_col + size(patch,2) - 1;
        padded_patch(start_row:end_row, start_col:end_col) = patch;
        patch = padded_patch;
    end
    
    % Apply transformation to canonical orientation
    output_size = [8 8];
    RA = imref2d(output_size, [0.5 8.5], [0.5 8.5]);
    transformed_patch = imwarp(patch, TForm, 'OutputView', RA);
    
    % Robust normalization to zero mean and unit variance
    descriptor = transformed_patch(:)';
    descriptor = descriptor - mean(descriptor);
    
    % Handle uniform patches
    patch_std = std(descriptor);
    if patch_std > eps
        descriptor = descriptor / patch_std;
    else
        descriptor(:) = 0; % Set to zero if no variation
    end
end