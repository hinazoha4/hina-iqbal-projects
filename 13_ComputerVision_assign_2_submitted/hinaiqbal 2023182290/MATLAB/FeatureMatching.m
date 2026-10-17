function [Matches] = FeatureMatching(Descpt1, Descpt2, Thresh, match_method)
    % Validate inputs
    if size(Descpt1, 2) ~= size(Descpt2, 2)
        error('Descriptor dimensions must match');
    end
    
    % Initialize matches
    Matches = struct('idx1', {}, 'idx2', {}, 'distance', {});
    
    % Compute pairwise distances
    D = pdist2(Descpt1, Descpt2, 'squaredeuclidean');
    
    switch lower(match_method)
        case 'ssd'
            % SSD Matching with additional checks
            for i = 1:size(Descpt1, 1)
                [min_dist, min_idx] = min(D(i,:));
                
                % Additional validation checks
                if min_dist <= Thresh && min_dist > eps
                    Matches(end+1) = struct(...
                        'idx1', i, ...
                        'idx2', min_idx, ...
                        'distance', min_dist);
                end
            end
            
        case 'ratio'
            % Ratio Test with improved robustness
            for i = 1:size(Descpt1, 1)
                [sorted_dists, sorted_idx] = sort(D(i,:));
                
                if length(sorted_dists) >= 2
                    ratio = sorted_dists(1) / sorted_dists(2);
                    
                    % Additional validation
                    if ratio <= Thresh && sorted_dists(1) > eps
                        Matches(end+1) = struct(...
                            'idx1', i, ...
                            'idx2', sorted_idx(1), ...
                            'distance', ratio);
                    end
                end
            end
            
        otherwise
            error('Unknown matching method. Use ''SSD'' or ''RATIO''');
    end
    
    % Sort matches by distance (ascending)
    if ~isempty(Matches)
        [~, idx] = sort([Matches.distance]);
        Matches = Matches(idx);
    end
end