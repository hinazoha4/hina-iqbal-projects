function [rhos, thetas] = HoughLines(H, nLines)
    % Define the neighborhood size for suppression
    neighborhoodSize = 5;  % Adjust based on resolution

    % Pad the accumulator to avoid boundary issues
    paddedH = padarray(H, [floor(neighborhoodSize/2), floor(neighborhoodSize/2)], 0, 'both');

    % Create a copy of H to modify
    H_suppressed = H;

    % Iterate through the Hough accumulator and apply non-maximal suppression
    for i = 1:size(H,1)
        for j = 1:size(H,2)
            % Define local region
            localRegion = paddedH(i:i+neighborhoodSize-1, j:j+neighborhoodSize-1);
            % Find the maximum value in the local region
            maxValue = max(localRegion(:));
            % Suppress non-maxima
            if H(i, j) < maxValue
                H_suppressed(i, j) = 0;
            end
        end
    end

    % Find the top nLines peaks in the suppressed accumulator
    [~, sortedIndices] = sort(H_suppressed(:), 'descend');
    topIndices = sortedIndices(1:nLines);
    
    % Convert linear indices to (rho, theta) coordinates
    [rhos, thetas] = ind2sub(size(H), topIndices);
end
