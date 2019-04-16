function output = evaluate_PCE(PCE, scenarios)
    %   EVALUATE_PCE evaluates a PCE for the given scenarios
    %
    %   output = EVALUATE_PCE(PCE, scenarios) calculates the result of
    %   evaluating the PCE given in the PCE structure for the supplied
    %   scenarios
    %   
    %   INPUT: 
    %           PCE: Structure containing all the information about the PCE
    %           Scenarios: The scenarios for which to sample the PCE [N x M
    %           matrix, where N is the number of scenarios and M the number
    %           of inputs in the PCE]
    %
    %   OUTPUT: 
    %           Output: The result of evaluating the PCE [N x K matrix, K
    %           is number of responses in PCE]

    %   This software is released under the <a href="matlab: 
    %   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
    %   Copyright (C) 2015  Sebastian van der Voort

    % Need to scale the scenarios because working in normalized coordinates
    scenarios = bsxfun(@rdivide, scenarios, PCE.std_devs);

    % Evaluate the polynomials themselves
    pol_val = evaluate_polynomial(PCE.pol_type, PCE.basis, transpose(scenarios));
    
    % Evaluating the polynomial gives us back a 3D matrix,  for all
    % indvidual inputs and polynomial types, need to take the product over
    % the different polynomials and reorder the matrix a bit for easy
    % calculation
%     pol_val = permute(prod(pol_val, 1), [3, 2, 1]);    
    
    % Finally the output is just the value of the polynomial times the PCE
    % coefficients
    output = PCE.coeffs*transpose(pol_val);
end
