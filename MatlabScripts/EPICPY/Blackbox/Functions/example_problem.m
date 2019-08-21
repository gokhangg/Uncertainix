function output = example_problem(input, optional_arguments)
%  EXAMPLE_PROBLEM is an example interface of the blackbox
%
%   output = EXAMPLE_PROBLEM(input, optional_arguments)
%   
%   INPUT: 
%          input: The points for which the blackbox should be evaluated [N
%          x M matrix, where N is the number of scenarios and M the number
%          of inputs]
%          optional_arguments: Optional arguments which can be passed to
%          the function [struct]
%
%   OUTPUT: 
%          output: The output of the blackbox model [N x K matrix, where N is
%          the number of scenarios and K is the number of outputs]

%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort
%     fileID = fopen('/scratch/ggunay/SourceCodesPython/PCE/Input.txt','w');
%     fprintf(fileID,'%.14f\n',2.^(input-9));
%     fclose(fileID);
%     input

    % The optional arguments are still string. If provided they need to be cast
    % to the appropiate file type (in this case a double).
    optional_arguments.problem_number = str2double(optional_arguments.problem_number);  
    
    % Multiple problems are defined here
    switch optional_arguments.problem_number
        case 1 
            % A very simple polynomial. The second index is the different inputs.
            output = input(:,1).^2 + 3*input(:,1)+ 6*input(:,2) +input(:,2).^3;
        case 2
            output = 3*input(:,1) + 2*input(:,2).^3 + 3*input(:,3) + 21;
    end
end