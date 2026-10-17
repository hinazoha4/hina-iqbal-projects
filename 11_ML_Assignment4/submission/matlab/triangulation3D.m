function pts3d = triangulation3D(P1, pts1, P2, pts2 )
% triangulation estimate the 3D positions of points from 2d correspondence
%   Args:
%       P1:     projection matrix with shape 3 x 4 for image 1
%       pts1:   coordinates of points with shape N x 2 on image 1
%       P2:     projection matrix with shape 3 x 4 for image 2
%       pts2:   coordinates of points with shape N x 2 on image 2
%
%   Returns:
%       Pts3d:  coordinates of 3D points with shape N x 3
%
    pts3d = zeros(length(pts1),3);

    p11 = P1(1,:);
    p12 = P1(2,:);
    p13 = P1(3,:);
    p21 = P2(1,:);
    p22 = P2(2,:);
    p23 = P2(3,:);

    for i=1:length(pts1)
        x1 = pts1(i,1);
        x2 = pts2(i,1);
        y1 = pts1(i,2);
        y2 = pts2(i,2);

        A = [y1*p13-p12; p11-x1*p13; y2*p23-p22; p21-x2*p23];
        
        [~,~,V] = svd(A);

        pts3d(i, :) = (V(1:3,end)')/V(end,end); 
    end
end


