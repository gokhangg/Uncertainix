% # *=========================================================================
% # *
% # *  Copyright Erasmus MC Rotterdam and contributors
% # *  This software is licensed under the Apache 2 license, quoted below.
% 
% # *  Copyright 2019 Erasmus MC Rotterdam.
% # *  Copyright 2019 Gokhan Gunay <g.gunay@erasmsumc.nl>
% 
% # *  Licensed under the Apache License, Version 2.0 (the "License"); you may not
% # *  use this file except in compliance with the License. You may obtain a copy of
% # *  the License at
% # *  http://www.apache.org/licenses/LICENSE-2.0
% 
% # *  Unless required by applicable law or agreed to in writing, software
% # *  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
% # *  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
% # *  License for the specific language governing permissions and limitations under
% # *  the License.
% # *=========================================================================


%brief: Parses input cell list.
%param: input Input cell list.
%return: Parsed parameters.
function out = commandlineParser(input)
    out.sizeInput = size(input);
    out.writePceWeights = false;
    out.runPCE = false;
    out.inVal = false;
    out.uncert = 0;
    out.verbose = false;
    out.direction = '';
    out.writePceWeightsFile = '';
    out.vectorLngth = 0;
    out.polOrder = 1;
    out.outDir = '';
    
    for ind = 1:out.sizeInput(2)
        if strcmp(input(ind),'-rootDir')
            out.rootDirInput = char(input(ind+1));
        end
        if strcmp(input(ind),'-outDir')
            out.outDir = char(input(ind+1));
        end

        if strcmp(input(ind),'-polOrderFile')
            out.polOrder = 1;
        end

        if strcmp(input(ind),'-settingsFile')
            out.settings_file = char(input(ind+1));
        end

        if strcmp(input(ind),'-runPCE')
            out.runPCE = true;
        end

        if strcmp(input(ind),'-writePceWeights')
            out.writePceWeights = true;
            out.writePceWeightsFile = char(input(ind+1));
        end

        if strcmp(input(ind),'-vectorLngth')
            out.vectorLngth = str2num(char(input(ind+1)));
        end

        if strcmp(input(ind),'-direction')
            out.direction = char(input(ind+1));
        end

        if strcmp(input(ind),'-inValuesText')
            out.inVal = true;
        end

        if strcmp(input(ind),'-uncertainty')
            out.uncert = true;
            out.requestedUncertGroupList = cmdLineUncertParser(input(ind+1));
        end

        if strcmp(input(ind),'-Evaluate')
            out.evaluate = true;
            out.evaluationFile = char(input(ind+1));
            display(out.evaluationFile);
        end
        
        if strcmp(input(ind),'-verbose')
            out.verbose = true;
        end
    end
end

%brief: Splits commandline argument after '-uncertainty' argument to find 
%which uncertainty combinations are requested. In the argument, '-' stands for
%separation indicator of uncertainty contribution parameter groups. '_'
%denotes which parameters to be considered to get uncertainty in a group.
%input: Commandline argument after '-uncertainty' argument.
%return: List of requests in cell format.
function out = cmdLineUncertParser(input)
	
    list = strsplit(char(input),'-');
    out = cell(1,numel(list));
	for ind = 1:numel(list);
        if (strcmp(list{ind},'all'))
            out(ind) = {'all'};
        else
            out(ind) = {splitUncertaintyGroup(list(ind))};
        end
    end
end

%brief: Returns which parameters are in a uncertainty contribtion group. 
%input: Uncertainty contribution group of parameters analyzed.
%return: Array of parameters to be analyzed in a uncertainty contribution
%group.
function out = splitUncertaintyGroup(input)

    list = strsplit(char(input),'_');
    out = [];
    for ind = 1:numel(list);
        ch = char(list(ind));
        out = cat(2,out,str2num(ch));
    end
end
