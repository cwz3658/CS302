function [] = LiveCoding_CA2()

plotOK = 1;

n = 256; % grid size
pop = zeros(n,n);
maxTime=10000; % simulation time

% discrete states: 0 = pop, 1 = soda, 2 = coke, 3 = tonic, 4 = soft drinks

% random inital conditions with majority
%pop(rand(n,n)<0.01) = 1;

% random inital conditions with uniformity
pop = rand(n,n);
pop(pop<0.2) = 0;
pop(pop>0 & pop<0.4) = 1;
pop(pop>0 & pop<1 & pop<0.6) = 2;
pop(pop>0 & pop<1 & pop<0.8) = 3;
pop(pop>0 & pop<1 & pop<1.0) = 4;


% segregated inital conditions
%pop(1:n/2,1:n/2) = 0;
%pop(n/2:end,1:n/2) = 1;
%pop(1:n/2,n/2:end) = 2;
%pop(n/2:end,n/2:end) = 4;


% visualize the simulation in figure(1)
figure(1);
axis equal
axis tight
axis square
% color map
clims = [-1 4];
cmap = [0.9,0.9,0.9; 0.8,0.2,0.2; 0.0,0.2,0.9; 0.2,0.8,0.2; 0.5,0.5,0.0; 0.0 0.0 0.0];

% metrics
ZEROS = sum(sum(pop==0))./(n*n);
ONES = sum(sum(pop==1))./(n*n);
TWOS = sum(sum(pop==2))./(n*n);
THREES = sum(sum(pop==3))./(n*n);
FOURS = sum(sum(pop==4))./(n*n);

% parameters
death = 1/75; %once every 75 years 
birth = 1;
hipster = 1/100;
[value coolest] = min([ZEROS, ONES, TWOS, THREES, FOURS]);

for t=1:maxTime
  
    %adaptive parameters
    [value coolest] = min([ZEROS, ONES, TWOS, THREES, FOURS]);
    coolest=coolest-1;

    %death events
    pop(rand(n,n)<death) = -1;

    %majority rule
    pop_births = ((pop(1:n,[n 1:n-1])==0) + (pop(1:n,[2:n 1])==0) + (pop([n 1:n-1], 1:n)==0) + (pop([2:n 1],1:n)==0));
    soda_births = ((pop(1:n,[n 1:n-1])==1) + (pop(1:n,[2:n 1])==1) + (pop([n 1:n-1], 1:n)==1) + (pop([2:n 1],1:n)==1));
    coke_births = ((pop(1:n,[n 1:n-1])==2) + (pop(1:n,[2:n 1])==2) + (pop([n 1:n-1], 1:n)==2) + (pop([2:n 1],1:n)==2));
    tonic_births = ((pop(1:n,[n 1:n-1])==3) + (pop(1:n,[2:n 1])==3) + (pop([n 1:n-1], 1:n)==3) + (pop([2:n 1],1:n)==3));
    soft_births = ((pop(1:n,[n 1:n-1])==4) + (pop(1:n,[2:n 1])==4) + (pop([n 1:n-1], 1:n)==4) + (pop([2:n 1],1:n)==4));
    
    pop(pop==-1 & pop_births>0 & pop_births>soda_births & pop_births>coke_births & pop_births>tonic_births & pop_births>soft_births) = 0;
    pop(pop==-1 & soda_births>0 & soda_births>pop_births & soda_births>coke_births & soda_births>tonic_births & soda_births>soft_births) = 1;
    pop(pop==-1 & coke_births>0 & coke_births>soda_births & coke_births>pop_births & coke_births>tonic_births & coke_births>soft_births) = 2;
    pop(pop==-1 & tonic_births>0 & tonic_births>soda_births & tonic_births>coke_births & tonic_births>pop_births & tonic_births>soft_births) = 3;
    pop(pop==-1 & soft_births>0 & soft_births>soda_births & soft_births>coke_births & soft_births>tonic_births & soft_births>pop_births) = 4;

    %hipster rule
    pop(pop == 0 & pop_births==4 & rand(n,n)<hipster) = coolest;
    pop(pop == 1 & soda_births==4 & rand(n,n)<hipster) = coolest;
    pop(pop == 2 & coke_births==4 & rand(n,n)<hipster) = coolest;
    pop(pop == 3 & tonic_births==4 & rand(n,n)<hipster) = coolest;
    pop(pop == 4 & soft_births==4 & rand(n,n)<hipster) = coolest;

    % metrics
    ZEROS = sum(sum(pop==0))./(n*n);
    ONES = sum(sum(pop==1))./(n*n);
    TWOS = sum(sum(pop==2))./(n*n);
    THREES = sum(sum(pop==3))./(n*n);
    FOURS = sum(sum(pop==4))./(n*n);
    
    if(plotOK)
        figure(1);
        imagesc(pop,clims); colormap(cmap);
        figure(2);
        plot(t,ZEROS,'r-o', t,ONES, 'b-o', t,TWOS, 'k-o', t,THREES, 'y-o', t,FOURS, 'g-o');
        hold on;
        drawnow
    end

end
figure(2);
hold off;
