function [H, rhoScale, thetaScale] = HoughTransform(Im, threshold, rhoRes, thetaRes)
    [rows, cols] = size(Im);
    
    % Calculate the rho and theta ranges
    diagLen = sqrt(rows^2 + cols^2);
    rhoMax = diagLen;
    rhoMin = -diagLen;
    rhoScale = rhoMin:rhoRes:rhoMax;   % rho scale
    thetaScale = -pi/2:thetaRes:pi/2;   % theta scale
    
    % Create Hough accumulator (initialized to 0)
    H = zeros(length(rhoScale), length(thetaScale));
    
    % Step 1: Detect edge pixels
    [y, x] = find(Im > threshold);  % Get indices of edge pixels
    
    % Step 2: Accumulate votes in Hough space
    for i = 1:length(x)
        for j = 1:length(thetaScale)
            theta = thetaScale(j);
            rho = round(x(i)*cos(theta) + y(i)*sin(theta));
            rhoIdx = round((rho - rhoMin) / rhoRes) + 1;
            if (rhoIdx > 0 && rhoIdx <= length(rhoScale))
                H(rhoIdx, j) = H(rhoIdx, j) + 1;
            end
        end
    end
end
