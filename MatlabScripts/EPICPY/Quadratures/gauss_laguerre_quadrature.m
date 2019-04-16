function [nodes, weights] = gauss_laguerre_quadrature(level, alpha)
%   GAUSS_LAGUERRE_QUADRATURE determines the nodes and weights for the
%   Gauss-LAGUERRE rule
%
%   nodes = GAUSS_LAGUERRE_QUADRATURE(level) computes the nodes for the
%   gauss-hermite rule corresponding to quadrature order level
%   [nodes, weights] = GAUSS_LAGUERRE_QUADRATURE(level) computes the nodes
%   and corresponding weights for the gauss-laguerre rule corresponding to
%   quadrature order level
%   
%   INPUT: 
%           level: Quadrature order for which to compute the quadrature
%           rule. The number of points returned is equal to level [Integer]
%           alpha: Alpha setting for Laguerre polynomial [float]
%
%   OUTPUT: 
%           nodes: Nodes for the gauss-hermite rule [level X 1 vector]
%           weights: Weights for the gauss-hermite rule [level X 1 vector]
%
%   See also LAGUERRE
%
%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort

% This function does net yet give back the same nodes + weights as FANISP,
% Need to investigate. It does give the expected nodes/weights for a
% gauss-laguerre quadrature

    if nargin < 2
        alpha = 0;
    end

    % Constructing the companion matrix based on the level, just need to
    % create the diagonals based on the recurrence relation
    i = 1:level;
    a = 2.*i - 1 + alpha;
    b = sqrt(i .* (i + alpha));
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