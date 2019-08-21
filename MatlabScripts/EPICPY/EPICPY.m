function PCE = EPICPY(settings_file)
%   EPICPY creates a polynomial chaos expansion of a problem
%
%   PCE = EPICPY(settings_file) construct the PCE based on the given
%   settings
%   
%   INPUT: 
%          settings_file: Name of settings file to use [String]
%   OUTPUT: 
%          PCE: The constructed polynomial chaos expansion [PCE struct]

%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort


    % Initialize the EPICPY enviroment
    initEPICPY()

    SettingsPCE = load_settings(settings_file);
    
    % Initialize the PCE structure
    PCE = struct();
    PCE.std_devs = SettingsPCE.std_devs;
    PCE.pol_type = SettingsPCE.pol_type;
    PCE.quadrature_type = SettingsPCE.quadrature_type;
    
    % First add the basis to the structure
    [PCE.basis, PCE.norm] = create_basis_PC(PCE, SettingsPCE);            
        
    % First get all the information about the cubature
    cubature = get_error_scenarios(SettingsPCE);
    
    % Calculate the response of the blackbox
    output = blackbox(SettingsPCE.blackbox_function, cubature.scenarios_scaled, SettingsPCE.optional_arguments);  
    numel(output)
   
    % Determine the coefficients    
    PCE.coeffs = calculate_coefficients(cubature, output, PCE, SettingsPCE);    
    
end
