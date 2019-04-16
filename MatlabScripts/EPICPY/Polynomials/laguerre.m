function [result, temp_recur] = laguerre(input, pol_orders, alpha)
%   LAGUERRE evaluates a Laguerre polynomial
%
%   result = LAGUERRE(input,pol_order) calculates the result of
%   evaluating a Laguerre polynomial with polynomial order pol_order at
%   the points input. 
%   
%   INPUT: 
%           input: Points at which to evaluate the Laguerre polynomial
%           [N x M matrix, N is number of inputs, M is number of scenarios]
%           pol_order: The UNIQUE polynomial orders of the Laguerre polynomial
%           [K x 1 vector, where K is the different polynomial orders]
%
%   OUTPUT: 
%           result: Result of evaluating the input for polynomial order
%           pol_order [length(input) X 1 vector]
%           temp_recur: Gives back not only the result for pol_order but
%           also for all lower orders [length(input) X pol_order + 1 matrix]
%   
%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2015  Sebastian van der Voort

    % Let's do a quick sanity check to see if the given polynomial orders
    % are unique
    
    if numel(pol_orders) ~= numel(unique(pol_orders))
        error('laguerre:noUniquePolynomials','This function only supports unique polynomial orders!')
    end

    N_input = size(input, 1);
    N_scenarios = size(input, 2);

    max_pol_order = max(pol_orders); 
    
    % Need to reshape a bit to get it conform the shape of temp_recur
    input = permute(input, [1, 3, 2]);
    
    if max_pol_order == 0
        result = ones(N_input, 1, N_scenarios);
    else
        temp_recur = ones(N_input, max_pol_order+1, N_scenarios); 
        temp_recur(:, 2, :) = 1 + alpha - input;  
        
        % The recurrence doesn't look exactly like the normal reccurence,
        % because we have to account for the fact that temp_recure(:,i,:)
        % is actually polynomial i - 1
        for i_pol = 3:max_pol_order + 1
            temp_recur(:, i_pol, :) = ...
                ((2.*i_pol + alpha - 3 - input).*temp_recur(:, i_pol - 1, :) ...
                - (i_pol + alpha - 2).*temp_recur(:, i_pol - 2, :))./(i_pol - 1);
        end
        
        % Finally just return the values that are actually requested
        result = temp_recur(:, pol_orders + 1, :);        
    end
end