function [Pts] = KeypointsDetection(img0, Pts)
    if ~isa(img0, 'double')
        img0 = im2double(img0);
    end
    
    % More meaningful scale space
    scales = [1.0, 1.6, 2.2, 3.0, 4.0]; % Geometric progression
    log_responses = zeros(size(img0, 1), size(img0, 2), length(scales));
    
    % Compute LoG responses
    for i = 1:length(scales)
        sigma = scales(i);
        hsize = 2*ceil(3*sigma) + 1;
        log_kernel = sigma^2 * fspecial('log', hsize, sigma); % Scale-normalized LoG
        log_responses(:,:,i) = abs(imfilter(img0, log_kernel, 'same', 'replicate'));
    end
    
    % Find dominant scale for each point
    for i = 1:length(Pts)
        x = min(max(round(Pts(i).x), 1), size(img0,2));
        y = min(max(round(Pts(i).y), 1), size(img0,1));
        
        [max_response, scale_idx] = max(log_responses(y, x, :));
        
        if max_response > eps % Only assign scale if significant response
            Pts(i).scale = scales(scale_idx);
        else
            Pts(i).scale = scales(1); % Default to smallest scale
        end
    end
    
    % More robust orientation calculation
    sigma_o = 1.5; % Typically 1.5×scale
    orientations = zeros(size(Pts));
    
    for i = 1:length(Pts)
        if isempty(Pts(i).scale) || Pts(i).scale < eps
            sigma = 1.5;
        else
            sigma = 1.5 * Pts(i).scale;
        end
        
        % Create Gaussian kernel adapted to scale
        kernel_size = 2*ceil(3*sigma) + 1;
        g = fspecial('gaussian', kernel_size, sigma);
        
        % Compute gradients in neighborhood
        x = round(Pts(i).x);
        y = round(Pts(i).y);
        radius = ceil(2*sigma);
        
        % Extract neighborhood with boundary checks
        xmin = max(1, x-radius);
        xmax = min(size(img0,2), x+radius);
        ymin = max(1, y-radius);
        ymax = min(size(img0,1), y+radius);
        
        patch = img0(ymin:ymax, xmin:xmax);
        if numel(patch) > 1
            % Compute gradients
            [Ix, Iy] = imgradientxy(patch, 'sobel');
            
            % Weight by Gaussian
            center = [radius+1, radius+1];
            [X, Y] = meshgrid(1:size(patch,2), 1:size(patch,1));
            weights = exp(-((X-center(1)).^2 + (Y-center(2)).^2)/(2*sigma^2));
            
            Ix_weighted = Ix .* weights;
            Iy_weighted = Iy .* weights;
            
            % Dominant orientation
            Pts(i).orientation = atan2d(sum(Iy_weighted(:)), sum(Ix_weighted(:)));
        else
            Pts(i).orientation = 0;
        end
    end
end