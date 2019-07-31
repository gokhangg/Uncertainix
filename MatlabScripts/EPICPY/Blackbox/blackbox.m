function output = blackbox(function_name, input, optional_arguments)
%   BLACKBOX forms the interface between the PCE construction and the
%   blackbox problem
%
%   output = BLACKBOX(function_name, input, optional_arguments)
%   
%   INPUT: 
%          function_name: Indicates which blackbox model to run [string]
%          input: The points for which the blackbox should be evaluated [N
%          x M matrix, where N is the number of scenarios and M the number
%          of inputs]
%          optional_arguments: Optional arguments which will be passed to
%          the function [struct]
%
%   OUTPUT: 
%          output: The output of the blackbox model [N x K matrix, where K
%          is the number of outputs]

%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort

    blackbox_function = str2func(function_name);
    try
        output = blackbox_function(input, optional_arguments);
    catch ME
        if strcmp(ME.identifier,'MATLAB:UndefinedFunction')
            error('blackbox:unknown_function',['The provided blackbox function "', function_name, '" could not be found. \n',...
                'Please make sure it is spelled correctly, and is in the EPICPY path.']);
        else
            rethrow(ME);
        end        
    end
end
