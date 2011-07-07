if 0
    Copyright (c) 2011, Aslak Grinsted
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in
          the documentation and/or other materials provided with the distribution

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
end

function noise=fftnoise(f,Nseries)
% Generate noise with a given power spectrum.
% Useful helper function for Monte Carlo null-hypothesis tests and confidence interval estimation.
%
% noise=fftnoise(f[,Nseries])
%
% INPUTS:
% f: the fft of a time series (must be a column vector)
% Nseries: number of noise series to generate. (default=1)
%
% OUTPUT:
% noise: surrogate series with same power spectrum as f. (each column is a surrogate).
%
% ------ Example: ------
% %calculate if the trend is significantly different from zero
% %(Null-hypothesis: a random process with the same power spectrum as data).
%
% x=(1:100)';
% data=smooth(randn(size(x)),15);
% pdata=polyfit(x,data,1)
% f=fft(data);
% psur=nan(length(pdata),10000);
% for ii=1:size(psur,2)
%   psur(:,ii)=polyfit(x,fftnoise(f),1)';
% end
% ptile=prctile(psur(1,:)',[2.5 97.5])
% if (pdata(1)>ptile(2))|(pdata(1)<ptile(1))
%   disp('significant trend')
% else
%   disp('not significant trend')
% end
%
%   --- Aslak Grinsted (2009)
if nargin<2
    Nseries=1;
end

f=f(:);
N=length(f);
Np=floor((N-1)/2);
phases=rand(Np,Nseries)*2*pi;
phases=complex(cos(phases),sin(phases)); % this was the fastest alternative in my tests.

f=repmat(f,1,Nseries);
f(2:Np+1,:)=f(2:Np+1,:).*phases;
f(end:-1:end-Np+1,:)=conj(f(2:Np+1,:));

noise=real(ifft(f,[],1));