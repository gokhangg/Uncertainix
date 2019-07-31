function basis_norm = calculate_norm(basis, pol_order, pol_type)
%   CALCULATE_NORM calculates the norm of basis vectors
%
%   basis_norm = CALCULATE_NORM(basis, pol_order, pol_type) 
%   
%   INPUT: 
%          basis: the basis vectors for which to determine the norm [N x M
%          matrix, where N is the number of basis vectors and M the number
%          of dimensions]
%          pol_order: The maximum polynomial order for the basis [integer]
%          pol_type: The polynomial types of the different dimensions [M x
%          1 cell array]
%
%   OUTPUT: 
%          basis_norm: The norm of the basis vectors [N x 1 array]

%   This software is released under the <a href="matlab: 
%   web('https://www.gnu.org/licenses/gpl-3.0.en.html')">GPLv3 license</a>.
%   Copyright (C) 2016  Sebastian van der Voort

    [u_pol_types, ~, I_u_pol_type] = unique(pol_type);  
    N_u_pol_types = numel(u_pol_types);
    N_basis_vectors = size(basis, 1);
    pol_order = double(pol_order);
    
    basis_norm = zeros(size(basis));
    
    for i_u_pol_type = 1:N_u_pol_types
       LI_cur_pol = i_u_pol_type == I_u_pol_type;
       N_cur_pols = nnz(LI_cur_pol);

       % Determine the basis norm just for the current polynomial type
       % Norms are such that the sum of weights is 1
       switch u_pol_types{i_u_pol_type}
           case 'hermite'
               cur_basis_norm = factorial(0:pol_order);
           case 'legendre'
               cur_basis_norm = 1./(2.*(0:pol_order)+1);
           case 'laguerre'
               cur_basis_norm = ones(1, pol_order+1);
           case 'jacobi'
               pol_orders = 0:pol_order;
               numerator = 0.5.*2.*gamma(pol_orders+1).*gamma(pol_orders+1);
               denominator = (2.*pol_orders + 1).*factorial(pol_orders).*gamma(pol_orders +1);
               cur_basis_norm = numerator./denominator;
          otherwise
               error('calculate_norm:unknownPolType','The requested polynomial type is not known');
       end % End switch over pol_types   
       
       % Determined for only one polynomial, need to expand to the actual number
       % of polynomials
       cur_basis_norm = repmat(cur_basis_norm, N_cur_pols, 1);
       
       % Then find the positions of the data we actually need
       I_dim = repmat(1:N_cur_pols, N_basis_vectors, 1);
       I_pol = basis(:, LI_cur_pol) + 1;       
       I_cur_to_full = sub2ind(size(cur_basis_norm), I_dim, I_pol);

       basis_norm(:, LI_cur_pol) = cur_basis_norm(I_cur_to_full);

    end % End for loop over pol_types
    
    % Now need the product over the different polynomials

    basis_norm = prod(basis_norm, 2); 
end
