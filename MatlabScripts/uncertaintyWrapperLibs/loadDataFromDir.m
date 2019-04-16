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

%brief: Loads input data from a directory.
%param: rootDirInput Directory where input data (deformation field) will be
%       sought.
%param: sz Number of datasets (deformation field images) to be loaded.
%return: All datasets.
function out = loadDataFromDir(rootDirInput,sz)
    
    fid = fopen(strcat(rootDirInput,'/NonRigid/Transformix',num2str(0),'/deformationField.mhd'),'r');
    out.mhdText = fscanf(fid,'%c');
    fclose(fid);
    
    fid = fopen(strcat(rootDirInput,'/NonRigid/Transformix',num2str(0),'/deformationField.raw'),'r');
    vol = single(fread(fid,'float'))';
    fclose(fid);
    out.data = zeros(sz(1),numel(vol),'single');
    out.data(1,:) = vol;
    for kk = 2:sz(1)
         fid = fopen(strcat(rootDirInput,'/NonRigid/Transformix',num2str(kk-1),'/deformationField.raw'),'r');
         vol = single(fread(fid,'float'))';
         fclose(fid);
         out.data(kk,:) = vol;
    end
end