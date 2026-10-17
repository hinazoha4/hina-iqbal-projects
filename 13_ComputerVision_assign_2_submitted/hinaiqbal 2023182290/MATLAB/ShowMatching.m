function ShowMatching(Match, img1, img2, Pts1, Pts2, Descpt1, Descpt2)
    % SHOWMATCHING Visualize and save match results with unique filenames
    % Inputs:
    %   Match    - Matching results (struct array with idx1, idx2)
    %   img1,img2- Images being compared  
    %   Pts1,Pts2- Keypoint structures (with x,y fields)
    %   Descpt1,Descpt2 - Descriptor matrices (not used in visualization)

    % 1. Ensure results directory exists
    results_dir = '../results';
    if ~exist(results_dir, 'dir')
        mkdir(results_dir);
        fprintf('Created directory: %s\n', results_dir);
    end

    % 2. Create composite image
    if size(img1, 3) == 1
        img1 = cat(3, img1, img1, img1);
    end
    if size(img2, 3) == 1
        img2 = cat(3, img2, img2, img2);
    end

    [h1, w1, ~] = size(img1);
    [h2, w2, ~] = size(img2);
    h = max(h1, h2);
    composite = zeros(h, w1+w2, 3);
    composite(1:h1, 1:w1, :) = img1; 
    composite(1:h2, w1+1:w1+w2, :) = img2;

    % 3. Create figure and display matches
    figure;
    imshow(composite);
    hold on;

    % Draw matches with small red circles and green lines
    for i = 1:length(Match)
        % Get coordinates with boundary checking
        idx1 = min(max(Match(i).idx1, 1), length(Pts1));
        idx2 = min(max(Match(i).idx2, 1), length(Pts2));
        
        x1 = min(max(Pts1(idx1).x, 1), w1);
        y1 = min(max(Pts1(idx1).y, 1), h1);
        x2 = min(max(Pts2(idx2).x, 1), w2) + w1;
        y2 = min(max(Pts2(idx2).y, 1), h2);

        % Small red circles (3px diameter)
        plot(x1, y1, 'ro', 'MarkerSize', 3, 'LineWidth', 1);
        plot(x2, y2, 'ro', 'MarkerSize', 3, 'LineWidth', 1);
        
        % Green connection line
        line([x1, x2], [y1, y2], 'Color', 'green', 'LineWidth', 1.5);
    end

    title(sprintf('Feature Matches (%d pairs)', length(Match)));
    hold off;

    % 4. Save with unique filename using timestamp
    timestamp = datestr(now, 'yyyymmdd_HHMMSS_FFF');
    filename = fullfile(results_dir, ['matches_', timestamp, '.png']);
    saveas(gcf, filename);
    fprintf('Saved matches to: %s\n', filename);
end