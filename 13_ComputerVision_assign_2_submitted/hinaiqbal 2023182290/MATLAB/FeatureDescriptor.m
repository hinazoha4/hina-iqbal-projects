function [Descriptors] = FeatureDescriptor(img0, Pts, descriptor_type, N)
    % Convert image to double if needed
    if ~isa(img0, 'double')
        img0 = im2double(img0);
    end
    
    % Initialize descriptors matrix
    num_points = length(Pts);
    
    switch lower(descriptor_type)
        case 'simple'
            % Simple 5x5 descriptor
            descriptor_size = 25;
            Descriptors = zeros(num_points, descriptor_size);
            
            for i = 1:num_points
                Descriptors(i,:) = SimpleFeatureDescriptor(img0, Pts(i));
            end
            
        case 's-mops'
            % MOPS descriptor (8x8)
            descriptor_size = 64;
            Descriptors = zeros(num_points, descriptor_size);
            
            for i = 1:num_points
                if nargin < 4 || isempty(N)
                    % Default patch size based on scale if N not provided
                    N = round(2 * Pts(i).scale * sqrt(2));
                    N = max(8, min(N, 40)); % Limit patch size
                end
                Descriptors(i,:) = MOPSFeatureDescriptor(img0, Pts(i), N);
            end
            
        otherwise
            error('Unknown descriptor type. Use ''Simple'' or ''S-MOPS''');
    end
end