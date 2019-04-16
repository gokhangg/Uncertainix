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

%brief: Writes weights table to a file.
%param: File File name to write the table.
%param: Table Table to write.
%return: NA.
function writeWeights(file,table)
    sz=size(table);
    fl_ = fopen(file,'w');
    display(file)
    fprintf(fl_,strcat(num2str(sz(1)),'\n'));
    for kk=1:sz(1)        
        for ii=1:sz(2)-1
            fprintf(fl_,char(strcat(num2str(table(kk,ii)),',')));
        end
        fprintf(fl_,char(strcat(num2str(table(kk,ii+1)),'\n')));
    end
    fprintf(fl_,'end of file');
    fclose(fl_);
end
