function SettingsPCE = load_settings(settings_file)
%   LOAD_SETTINGS loads a json file with the settings for the PCE construction
%
%   SettingsPCE = load_settings(settings_file) returns the settings specified in
%   the settings file
%   
%   INPUT: 
%          settings_file: Name of settings file to use [String]
%   OUTPUT: 
%         SettingsPCE: Structure with the settings for PCE construction [Struct]

%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort

    SettingsPCE = loadjson(settings_file);
    
    % Settings load from json are strings, need to convert it to appropiate 
    % types    
    SettingsPCE.pol_order = uint8(str2double(SettingsPCE.pol_order));
    SettingsPCE.grid_level = uint8(str2double(SettingsPCE.grid_level));
    SettingsPCE.std_devs = str2double(SettingsPCE.std_devs);
    SettingsPCE.trim = logical(SettingsPCE.trim);
    SettingsPCE.remove_small_elements = logical(SettingsPCE.remove_small_elements);
    SettingsPCE.threshold = str2double(SettingsPCE.small_element_threshold);  
end