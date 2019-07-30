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

function pceExe(varargin)
    addpath(strcat(pwd,'/MatlabScripts/EPICPY'));

    %input argument parsing
    pars = commandlineParser(varargin);
    %read settings file and init PCE
    SettingsPCE = load_settings(pars.settings_file);
    if (pars.verbose)
        display('PCE setting file read')    
    end
    PCE = struct();
    PCE.std_devs = SettingsPCE.std_devs;
    PCE.pol_type = SettingsPCE.pol_type;
    PCE.quadrature_type = SettingsPCE.quadrature_type; 
    
    % First add the basis to the structure
    [PCE.basis, PCE.norm] = create_basis_PC(PCE, SettingsPCE);            
    % First get all the information about the cubature
    cubature = get_error_scenarios(SettingsPCE);
    
    %if PCE parameter sampling locations are requested for registration
    % parameters to be analyzed.
    if (pars.writePceWeights)
        writeWeights(pars.writePceWeightsFile,cubature.scenarios_scaled)
        if (pars.verbose)
            display(strcat('Weight value file has been written as ',pars.writePceWeightsFile));
        end
    end

    %check if execution of PCE algorithm is requested.
    if (pars.runPCE)
        %get sample size from the PCE settings and load dataset sampled 
        %from output of the model analyzed.
        sampleSize = size(cubature.scenarios_scaled);
        dataLoaded = loadDataFromDir(pars.rootDirInput,sampleSize);
        display(dataLoaded.data);
        MhdText=dataLoaded.mhdText;
        ParamAll = dataLoaded.data;
        if (pars.verbose)
            display('All input data read')
        end
        
        %calculate PCE model coefficients from loaded dataset.
        PCE.coeffs = calculate_coefficients(cubature, ParamAll, PCE, SettingsPCE);
        if (pars.verbose)
            display('PCE constructed')
        end

        %check if uncertainty estimation is requested.
        if (pars.uncert)
                %calculate uncertainties as per the list provided in 
                %pars.requestedUncertGroupList
                for ind = 1:numel(pars.requestedUncertGroupList)
                    list = pars.requestedUncertGroupList{ind};
                    if (strcmp(list,'all'))
                        str='All';
                    else
                        str = num2str(list(1));
                        for ind2 = 2:numel(list)
                            str = strcat(str,'_',num2str(list(ind2)));
                        end
                    end
                    
                    %get uncertainty image for combination in list "pars.requestedUncertGroupList".
                    uncertImageRawData = handleUncertaintyRequests(list,PCE.coeffs,PCE.basis);
                    
                    %write estimated uncertainty image.
                    outFileName = char(strcat(pars.outDir,'/Unc',str,'Gl',num2str(SettingsPCE.grid_level),'Po',num2str(SettingsPCE.pol_order)));
                    mhdTextOut = strcat(MhdText(1:strfind(MhdText,'ElementDataFile')),'lementDataFile = ','Unc',str,'Gl',num2str(SettingsPCE.grid_level),'Po',num2str(SettingsPCE.pol_order),'.raw');
                    writeUncertaintyImage(outFileName,uncertImageRawData,mhdTextOut);
                
                end
            if (pars.verbose)
                display('Uncertainty written') 
            end
        end
        if (pars.evaluate)
                %calculate uncertainties as per the list provided in
                %pars.requestedUncertGroupList
                scenarios=handleEvaluationFile(pars.evaluationFile);
                display(scenarios(1,:))
                sz_scenarios=size(scenarios);
                for ind = 1:sz_scenarios(1)
                    %get uncertainty image for combination in list "pars.requestedUncertGroupList".
                    evaluationImageData = evaluate_PCE(PCE,scenarios(ind,:));

                    %write estimated evaluation image.
                    fileName=char(strcat('Gl',num2str(SettingsPCE.grid_level),'Po',num2str(SettingsPCE.pol_order),'Scen',num2str(ind)));
                    fullFileName = char(strcat(pars.outDir,'/',fileName));
                    mhdTextOut = strcat(MhdText(1:strfind(MhdText,'ElementDataFile')),'lementDataFile = ',fileName,'.raw');
                    writeUncertaintyImage(fullFileName,evaluationImageData,mhdTextOut);

                end
            if (pars.verbose)
                display('Evaluation images written')
            end
        end
    end
end
