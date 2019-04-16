function [nodes, weights] = gauss_jacobi_quadrature(level, alpha, beta)
%   GAUSS_JACOBI_QUADRATURE determines the nodes and weights for the
%   Gauss-Jacobi rule
%
%   nodes = GAUSS_JACOBI_QUADRATURE(level) computes the nodes for the
%   gauss-jacobi rule corresponding to quadrature order level
%   [nodes, weights] = GAUSS_JACOBI_QUADRATURE(level) computes the nodes
%   and corresponding weights for the gauss-jacobi rule corresponding to
%   quadrature order level
%   
%   INPUT: 
%           level: Quadrature order for which to compute the quadrature
%           rule. The number of points returned is equal to level [Integer]
%           alpha: Alpha setting for Jacobi polynomial [float]
%           beta: Beta setting for Jacobi polynomial [float]
%
%
%   OUTPUT: 
%           nodes: Nodes for the gauss-jacobi rule [level X 1 vector]
%           weights: Weights for the gauss-jacobi rule [level X 1 vector]
%
%   See also JACOBI
%
%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort

    if nargin < 2
        alpha = 0;
        beta = 0;
    end

    % Constructing the companion matrix based on the level, just need to
    % create the diagonals based on the recurrence relation
    i = 1:level;
    nu = alpha + beta;
    a = (beta^2 - alpha^2)./(4.*i.^2 + 4.*i.*nu + nu.^2 - 4.*i - 2*nu);
    % With jacobi for i = 1 we always get a = Inf/NaN because of
    % denominator, if alpha=beta=0, fix that here:
    
    if alpha == 0 && beta == 0
        a(1) = 0;
    end
        
    b = sqrt((4.*(i+alpha).*(i+beta).*i.*(i+nu))./((2.*i+nu).^2 .* (2.*i + nu - 1).*(2.*i + nu + 1)));
    % Cut off last element of b, don't need it
    b = b(1:level-1);
    
    companion_mat = diag(b, -1) + diag(a, 0) + diag(b, 1);
        
    [eigenVec, eigenVal] = eig(companion_mat,'vector');
    
    % Nodes are eigenvalues of the companion matrix
    [nodes, index] = sort(eigenVal);

    % The corresponding (normalized) weights are just the first element of the eigen
    % vector squared.
    weights = transpose(eigenVec(1,index).^2);
end