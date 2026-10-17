function [Pts] = HarrisCorner(img0, thresh, sigma_d, sigma_i, NMS)
    % Convert image to double if needed
    if ~isa(img0, 'double')
        img0 = im2double(img0);
    end
    
    % Create Gaussian derivative kernels with proper normalization
    hsize = max(3, 2*ceil(3*sigma_d)+1); % Ensure odd size ≥ 3
    [x, y] = meshgrid(-(hsize-1)/2:(hsize-1)/2, -(hsize-1)/2:(hsize-1)/2);
    
    % Properly normalized Gaussian derivatives
    Gx = -x .* exp(-(x.^2 + y.^2)/(2*sigma_d^2)) / (sqrt(2*pi)*sigma_d^3);
    Gy = -y .* exp(-(x.^2 + y.^2)/(2*sigma_d^2)) / (sqrt(2*pi)*sigma_d^3);
    
    % Compute image gradients with border replication
    Ix = imfilter(img0, Gx, 'same', 'replicate');
    Iy = imfilter(img0, Gy, 'same', 'replicate');
    
    % Gaussian window for integration
    g = fspecial('gaussian', max(3, 2*ceil(3*sigma_i)+1), sigma_i);
    
    % Compute structure tensor components
    Ix2 = conv2(Ix.^2, g, 'same');
    Iy2 = conv2(Iy.^2, g, 'same');
    IxIy = conv2(Ix.*Iy, g, 'same');
    
    % Improved corner response calculation
    k = 0.04;
    traceH = Ix2 + Iy2;
    detH = Ix2.*Iy2 - IxIy.^2;
    
    % Avoid division by zero for flat regions
    corner_response = detH - k*(traceH.^2);
    corner_response(traceH < eps) = 0; % Flat regions
    
    % Adaptive thresholding
    valid_mask = ~isnan(corner_response) & ~isinf(corner_response);
    if any(valid_mask(:))
        max_response = max(corner_response(valid_mask));
        threshold = thresh * max_response;
        c_binary = corner_response > threshold;
    else
        c_binary = false(size(corner_response));
    end
    
    % Improved non-maximum suppression
    if NMS > 0
        se = strel('square', NMS);
        c_localmax = imregionalmax(corner_response);
        c_binary = c_binary & c_localmax;
    end
    
    % Get coordinates and create structure
    [y, x] = find(c_binary);
    Pts = struct('x', num2cell(x), 'y', num2cell(y), 'scale', [], 'orientation', []);
end