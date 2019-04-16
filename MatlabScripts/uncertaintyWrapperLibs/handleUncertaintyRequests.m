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


%brief: used in uncertainty estimations. It returns uncertainty estimates
%       for analyzed input parameters.
%param: paramsToAnalyze Combination of parameters to be analyzed.
%       Instance: "1_2" or "all" mean combination of the parameters 1 and 2
%       or all parameters (overall uncertainty), respectively.
%param: pceCoeffs Estimated PCE coefficients.
%param: pceBasis PCE basis as per which the model is constructed.
%return: Uncertainty image.
function out=handleUncertaintyRequests(paramsToAnalyze,pceCoeffs,pceBasis)


    %first column of the pce coefficients are of c_0 coefficient and to be
    %omitted
    pceCoeffsTrim = pceCoeffs(:,2:end);
    %first row of the pce coefficients are of c_0 coefficient and to be
    %omitted
    pceBasisTrim = pceBasis(2:end,:);
    
    coeffSquare = pceCoeffsTrim.*pceCoeffsTrim;
    basisVect = coeffVect(paramsToAnalyze,pceBasisTrim);
    out = single(sqrt(coeffSquare*basisVect));
end
    

function out = coeffVect(paramsToAnalyze,pceBasis)

    szPceBasis = size(pceBasis);
    out = single(zeros(szPceBasis(1),1));    
    for ind = 1:szPceBasis(1)
        if (strcmp(paramsToAnalyze,'all'))
            out(ind) = getFactorials(pceBasis(ind,:));
        else
            if (checkBasis(paramsToAnalyze,pceBasis(ind,:)))
                out(ind) = getFactorials(pceBasis(ind,:));
            else
                out(ind) = 0;
            end
        end
        
    end
end
    

function out = checkBasis(paramsToAnalyze,basisVect)

    basisVectSel = 0*basisVect;
    for ind = 1:numel(paramsToAnalyze)
        basisVectSel(paramsToAnalyze(ind)) = true;
    end
    xr = xor(basisVectSel,basisVect>0);
    if (sum(xr)>0)
        out = false;
    else
        out = true;
    end
end

function out = getFactorials(basisVect)

    out = 1.;
    for ind = 1:numel(basisVect) 
        out = out*factorial(basisVect(ind));
    end
end
