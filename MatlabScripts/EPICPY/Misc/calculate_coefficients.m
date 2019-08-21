function coefficients = calculate_coefficients(cubature, output, PCE, SettingsPCE)
%   CALCULATE_COEFFIENTS calculations the expansion coefficients of a PCE
%
%   coefficients = calculate_coefficients(cubature, output, PCE)
%   
%   INPUT: 
%           cubature: the cubatures to be used [cubature structure]
%           output: the blackbox model evaluated at the cubature nodes [N x
%           M matrix, where N is the number of nodes and M is the number of outputs]
%           PCE: contains information about the PCE [PCE structure]
%
%   OUTPUT: 
%          coefficients: The calculated coefficients of the expansion [M x
%          K matrix, where K is the number of basis vectors]

%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort

        % First calculate the polynomial value for all scenarios
        pol_val = evaluate_polynomial(PCE.pol_type, PCE.basis, transpose(cubature.scenarios));

        coefficients = transpose(output)*bsxfun(@times, pol_val, cubature.total_weights);
        coefficients = bsxfun(@rdivide, coefficients, transpose(PCE.norm));
        
        if SettingsPCE.remove_small_elements
            coefficients(abs(coefficients) < SettingsPCE.threshold) = 0;
        end
end
