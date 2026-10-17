function [img1] = EdgeFilter(img0, sigma)
    % Gaussian filter kernel size based on sigma
    hsize = 2 * ceil(3 * sigma) + 1; 
    h = fspecial('gaussian', hsize, sigma);  % Create Gaussian filter
    
    % Step 1: Smooth the image using the Gaussian filter
    smoothedImg = ImageFilter(img0, h); 
    
    % Sobel filters for gradient calculation
    Gx = [-1, 0, 1; -2, 0, 2; -1, 0, 1];  % Sobel filter for x gradient
    Gy = [-1, -2, -1; 0, 0, 0; 1, 2, 1];   % Sobel filter for y gradient
    
    % Step 2: Compute gradients
    imgx = ImageFilter(smoothedImg, Gx);  % Gradient in x-direction
    imgy = ImageFilter(smoothedImg, Gy);  % Gradient in y-direction
    
    % Step 3: Calculate the magnitude and direction of the gradients
    magnitude = sqrt(imgx.^2 + imgy.^2);  % Gradient magnitude
    direction = atan2(imgy, imgx);        % Gradient direction
    
    % Step 4: Perform Non-Maximum Suppression (NMS)
    img1 = NonMaximumSuppression(magnitude, direction);
end

