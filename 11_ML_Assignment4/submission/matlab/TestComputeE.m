load('../data/intrinsics.mat'); 
load('../data/correspondences.mat');


F = computeF(pts1, pts2);
E = computeE(F, K1, K2);
disp('Computed Essential Matrix:');
disp(E);
[U, S, V] = svd(E);
disp('Singular values of E (should be [a, b, 0]):');
disp(diag(S)');
disp(['Rank of E: ', num2str(rank(E))]);