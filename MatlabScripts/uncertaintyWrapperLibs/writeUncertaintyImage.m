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

%brief: Writes uncertainty image as mhd image.
%param: pars.requestedUncertGroupList Name of the mhd file without 
%       extention. File extentions are concatenated later.
%param: rawData Image raw data.
%param: mhdText Text to be put in the mhd header file.
%return: NA.
function writeUncertaintyImage(fileNameWithoutExtension,rawData,mhdText)
    fl = fopen(strcat(fileNameWithoutExtension,'.raw'),'w');
    fwrite(fl,rawData,'float');
    fclose(fl);
    fid = fopen(strcat(fileNameWithoutExtension,'.mhd'),'w');
    fprintf(fid,'%c',mhdText);
    fclose(fid);
end