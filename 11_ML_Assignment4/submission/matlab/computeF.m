function F = computeF(pts1, pts2)
    % COMPUTEF Compute the fundamental matrix from point correspondences
    %   pts1 and pts2 are N×2 matrices of corresponding points.

    N = size(pts1,1);
    % Normalize data points
    c1 = mean(pts1);
    c2 = mean(pts2);
    pts1n = pts1 - c1;
    pts2n = pts2 - c2;
    d1 = mean(sqrt(sum(pts1n.^2,2)));
    d2 = mean(sqrt(sum(pts2n.^2,2)));
    s1 = sqrt(2)/d1;
    s2 = sqrt(2)/d2;
    T1 = [s1 0 -s1*c1(1); 0 s1 -s1*c1(2); 0 0 1];
    T2 = [s2 0 -s2*c2(1); 0 s2 -s2*c2(2); 0 0 1];

    % Homogeneous coordinates
    pts1h = [pts1 ones(N,1)]';
    pts2h = [pts2 ones(N,1)]';

    % Apply normalization
    pts1n = T1 * pts1h;
    pts2n = T2 * pts2h;
    x1 = pts1n(1,:)'; y1 = pts1n(2,:)';
    x2 = pts2n(1,:)'; y2 = pts2n(2,:)';

    % Build linear system A f = 0
    A = [x2.*x1, x2.*y1, x2, y2.*x1, y2.*y1, y2, x1, y1, ones(N,1)];

    % Solve using SVD
    [~,~,V] = svd(A);
    f = V(:,end);
    Fn = reshape(f,3,3)';

    % Enforce rank-2 constraint
    [U,S,Vf] = svd(Fn);
    S(3,3) = 0;
    Fn2 = U * S * Vf';

    % Optional refinement (uncomment if refineF is available)
    % Fn2 = refineF(Fn2, pts1, pts2);

    % Denormalize
    F = T2' * Fn2 * T1;

    % Normalize so that F(3,3) = 1
    F = F / F(3,3);
end