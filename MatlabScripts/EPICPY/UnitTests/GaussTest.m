classdef GaussTest < matlab.unittest.TestCase   
    % Unit tests for Gaussian quadrature
    methods (Test)
        function testZeroOrder(testCase)
            [actNode, actWeight] = gauss_hermite_quadrature(0);
            expNode = 0;
            expWeight = 1;
            testCase.verifyEqual(actNode,expNode);
            testCase.verifyEqual(actWeight,expWeight);
        end
        
        
        function testThirdOrder(testCase)
            [actNode, actWeight] = gauss_hermite_quadrature(3);
            
            expNode = [-1.732050;...
                       0;...
                       1.732050];
            
            
            expWeight = [0.166667;...
                         0.666667;...
                         0.166667];
                     
            testCase.verifyEqual(size(actNode,1), 3)
            testCase.verifyEqual(size(actNode,2), 1)
            testCase.verifyEqual(size(actWeight,1), 3)
            testCase.verifyEqual(size(actWeight,2), 1)
            testCase.verifyEqual(actNode,expNode,'AbsTol',1e-6);
            testCase.verifyEqual(actWeight,expWeight,'AbsTol',1e-6);
        end        
        
        function testFifthOrder(testCase)
            [actNode, actWeight] = gauss_hermite_quadrature(5);
            
            expNode = [-2.856970;...
                       -1.355626;...
                       0;...
                       1.355626;...
                       2.856970];
            
            
            expWeight = [0.011257;...
                         0.222076;...
                         0.533333;...
                         0.222076;...
                         0.011257];
                     
            testCase.verifyEqual(size(actNode,1), 5)
            testCase.verifyEqual(size(actNode,2), 1)
            testCase.verifyEqual(size(actWeight,1), 5)
            testCase.verifyEqual(size(actWeight,2), 1)
            testCase.verifyEqual(actNode,expNode,'AbsTol',1e-6);
            testCase.verifyEqual(actWeight,expWeight,'AbsTol',1e-6);
        end
    end 
end 