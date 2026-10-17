function [output] = NonMaximumSuppression(magnitude, direction)
    [rows, cols] = size(magnitude);
    output = zeros(rows, cols);  % Initialize the output image
    
    % Quantize the gradient direction to 8 angles (in radians)
    for i = 2:rows-1    % Start from the second row and end at the second to last row
        for j = 2:cols-1 % Start from the second column and end at the second to last column
            angle = direction(i, j);
            
            % Normalize angle to be between 0 and pi
            if angle < 0
                angle = angle + pi;
            end
            angle = mod(angle, pi);  % Ensure it's between 0 and pi
            
            % Quantize the angle into 8 main directions (0°, 45°, 90°, 135°)
            if (angle >= 0 && angle < pi/8) || (angle >= 7*pi/8 && angle < pi)
                % 0 degrees (horizontal edge)
                neighbor1 = magnitude(i, j-1); % Left
                neighbor2 = magnitude(i, j+1); % Right
            elseif (angle >= pi/8 && angle < 3*pi/8)
                % 45 degrees (top-left to bottom-right)
                neighbor1 = magnitude(i-1, j-1); % Top-left
                neighbor2 = magnitude(i+1, j+1); % Bottom-right
            elseif (angle >= 3*pi/8 && angle < 5*pi/8)
                % 90 degrees (vertical edge)
                neighbor1 = magnitude(i-1, j);   % Top
                neighbor2 = magnitude(i+1, j);   % Bottom
            elseif (angle >= 5*pi/8 && angle < 7*pi/8)
                % 135 degrees (top-right to bottom-left)
                neighbor1 = magnitude(i-1, j+1); % Top-right
                neighbor2 = magnitude(i+1, j-1); % Bottom-left
            end
            
            % Non-Maximum Suppression
            if (magnitude(i, j) > neighbor1 && magnitude(i, j) > neighbor2)
                output(i, j) = magnitude(i, j);
            else
                output(i, j) = 0;
            end
        end
    end
end
