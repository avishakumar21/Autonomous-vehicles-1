%{
    ECE 6680 - Final Project
    @author Tyler S. Sherman
    @date 05.18.2020
    @version 01
%}
%*************************************************************************%
%                             IMPORT & REFORMAT                           %
%*************************************************************************%
collisions_per_sim = {1, 9};
speed_per_sim      = {1, 9};
accel_per_sim      = {1, 9};

%{
    Autonomous Vehicle with V2V: V2V
    Human Driver: human
    Autonomous Vehicle without V2V: AV
%}

files = {'../20 trials/V2Vpedestrian.csv', '../20 trials/V2Vems.csv', '../20 trials/V2Vpothole.csv', '../20 trials/Humanpedestrian.csv', '../20 trials/Humanems.csv', '../20 trials/Humanpothole.csv', '../20 trials/AVpedestrian.csv', '../20 trials/AVems.csv', '../20 trials/AVpothole.csv'};
for file_number = 1:length(files)
    % Import data from CSV
    % COLUMNS = time,   ID,  accel,  vel,   pos,  collisions
    M = readtable(char(files(1, file_number)));
    sim_length = height(M);
    
    % TIME
    time = table2array(M(:,1));
    for i = 1:length(time)
        time(i) = round(time(i), 1, 'decimal');
    end
    t_start  = 0.0;
    t_end    = 19.9;

    % ID
    id = table2array(M(:,2));

    % ACCELERATION
    accel = table2array(M(:,3));

    % SPEED & VELOCITY
    vel   = table2array(M(:,4));
    x_vel = zeros(sim_length, 1);
    y_vel = zeros(sim_length, 1);
    for i = 1:sim_length
        temp_vel = vel{i};
        temp_split = split(temp_vel, ["(",","," ",")"]);
        x_vel_temp = str2double(temp_split{2});
        y_vel_temp = str2double(temp_split{4});
        if abs(x_vel_temp) < 1e-5
            x_vel_temp = 0.0;
        end
        if abs(y_vel_temp) < 1e-5
            y_vel_temp = 0.0;
        end
        x_vel(i) = x_vel_temp;
        y_vel(i) = y_vel_temp;
    end
    speed = sqrt(x_vel.^2 + y_vel.^2);

    % POSITION
    pos = table2array(M(:,5));
    x_pos = zeros(sim_length, 1);
    y_pos = zeros(sim_length, 1);
    for i = 1:sim_length
        temp_pos = pos{i};
        temp_split = split(temp_pos, ["(",","," ",")"]);
        x_pos(i) = str2double(temp_split{2});
        y_pos(i) = str2double(temp_split{4});
    end

    % Collisions
    collisions = table2array(M(:,6));

    % Recombine data into matrix
    %{
        1:  Time
        2:  ID
        3:  Acceleration
        4:  Speed
        5:  Collisions
    %}
    Data = [time, id, accel, speed, collisions];

%*************************************************************************%
%                           SPLIT DATA BY TRIAL                           %
%*************************************************************************%
    % Time start = 0.0
    % Time end   = 19.9
    % Num trials = 20
    
    % Find the index where one trial ends & the next begins
    counter = 1;
    num_trials = 20;
    end_index = zeros(num_trials, 1);
    for i = 2:sim_length
        cur_time  = Data(i, 1);
        prev_time = Data(i-1, 1);
        if((cur_time==t_start) && (prev_time==t_end))
            end_index(counter) = i-1;
            counter = counter+1;
        end
    end
    end_index(20) = sim_length;
    
    % Split the data
    Data_trial = {1, 20};
    start_i = 1;
    for i = 1:20
        end_i   = end_index(i);
        
        cur_trial = Data(start_i:end_i, :);
        Data_trial{i} = cur_trial;
        
        start_i = end_i+1;
    end

%*************************************************************************%
%                           COLLISION STATISTICS                          %
%*************************************************************************%
    num_collisions = zeros(20, 1);
    for i = 1:20
        % Last row has the total final number of collisions
        num_collisions(i) = Data_trial{i}(length(Data_trial{i}), 5);
    end
    collisions_per_sim{file_number} = num_collisions;
    
%*************************************************************************%
%                              SPEED STATISTICS                           %
%*************************************************************************%
    avg_speed = zeros(20, 1);
    for i = 1:20
        avg_speed(i) = mean(Data_trial{i}(:, 4));
    end
    speed_per_sim{file_number} = avg_speed;

%*************************************************************************%
%                           ACCELERATION STATISTICS                       %
%*************************************************************************%
    avg_accel = zeros(20, 1);
    for i = 1:20
        avg_accel(i) = mean(Data_trial{i}(:, 3));
    end
    accel_per_sim{file_number} = avg_accel;
    
end

clearvars -except collisions_per_sim speed_per_sim accel_per_sim

% %% PLOTTING COLLISIONS
% % Sub-plot 1: Pedestrian Crossing Scenario 
% figure
% subplot(1,3,1)
% V2V   = [collisions_per_sim{1}];
% H     = [collisions_per_sim{4}];
% AV    = [collisions_per_sim{7}];
% group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
% boxplot([V2V; H; AV], group)
% % Plot Properties
% title('Pedestrian Crossing Scenario')
% set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
% xlabel('Vehicle Type')
% ylabel('Number of Collisions')
% 
% % Sub-plot 2: EMS Scenario
% subplot(1,3,2)
% V2V   = [collisions_per_sim{2}];
% H     = [collisions_per_sim{5}];
% AV    = [collisions_per_sim{8}];
% group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
% boxplot([V2V; H; AV], group)
% % Plot Properties
% title('EMS Scenario')
% set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
% xlabel('Vehicle Type')
% ylabel('Number of Collisions')
% 
% % Sub-plot 3: Pothole Scenario
% subplot(1,3,3)
% V2V   = [collisions_per_sim{3}];
% H     = [collisions_per_sim{6}];
% AV    = [collisions_per_sim{9}];
% group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
% boxplot([V2V; H; AV], group)
% % Plot Properties
% title('Pothole Scenario')
% set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
% xlabel('Vehicle Type')
% ylabel('Number of Collisions')
% 
% % Figure Title
% plotTitle = sprintf('Vehicle Collisions\n');
% sgt = sgtitle(plotTitle,'Color','red');
% sgt.FontSize = 20;

%% PLOTTING COLLISIONS - ALTERNATE
figure
y = [mean(collisions_per_sim{1}), mean(collisions_per_sim{4}), mean(collisions_per_sim{7}); mean(collisions_per_sim{2}), mean(collisions_per_sim{5}), mean(collisions_per_sim{8}); mean(collisions_per_sim{3}), mean(collisions_per_sim{6}), mean(collisions_per_sim{9})];
bar(y);
% Plot Properties
%title('Average Number of Vehicle Collisions over 20 Trials')
set(gca,'xticklabel',{'Animal Crossing','Emergency Responder','Pothole'});
xlabel('Scenario')
ylabel('Number of Collisions')
grid on
legend('AV with V2V', 'Human', 'AV without V2V', 'location', 'northeast');

%% PLOTTING VEHICLE SPEEDS
% Sub-plot 1: Pedestrian Crossing Scenario 
figure
subplot(3,1,1)
V2V   = [speed_per_sim{1}];
H     = [speed_per_sim{4}];
AV    = [speed_per_sim{7}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Animal Crossing')
set(gca,'XTickLabel',{'AV with V2V','Human','AV without V2V'})
xlabel('Vehicle Type')
ylabel('Speed (m/s)')

% Sub-plot 2: EMS Scenario
subplot(3,1,2)
V2V   = [speed_per_sim{2}];
H     = [speed_per_sim{5}];
AV    = [speed_per_sim{8}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Emergency Responder')
set(gca,'XTickLabel',{'AV with V2V','Human','AV without V2V'})
xlabel('Vehicle Type')
ylabel('Speed (m/s)')

% Sub-plot 3: Pothole Scenario
subplot(3,1,3)
V2V   = [speed_per_sim{3}];
H     = [speed_per_sim{6}];
AV    = [speed_per_sim{9}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Pothole')
set(gca,'XTickLabel',{'AV with V2V','Human','AV without V2V'})
xlabel('Vehicle Type')
ylabel('Speed (m/s)')

% Figure Title
%plotTitle = sprintf('Vehicle Speeds\n');
%sgt = sgtitle(plotTitle,'Color','red');
%sgt.FontSize = 20;

%% PLOTTING VEHICLE ACCELERATIONS
% Sub-plot 1: Pedestrian Crossing Scenario 
figure
subplot(3,1,1)
V2V   = [accel_per_sim{1}];
H     = [accel_per_sim{4}];
AV    = [accel_per_sim{7}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Pedestrian Crossing Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Acceleration (m/s^2)')

% Sub-plot 2: EMS Scenario
subplot(3,1,2)
V2V   = [accel_per_sim{2}];
H     = [accel_per_sim{5}];
AV    = [accel_per_sim{8}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('EMS Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Acceleration (m/s^2)')

% Sub-plot 3: Pothole Scenario 
subplot(3,1,3)
V2V   = [accel_per_sim{3}];
H     = [accel_per_sim{6}];
AV    = [accel_per_sim{9}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Pothole Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Acceleration (m/s^2)')

% Figure Title
plotTitle = sprintf('Vehicle Accelerations\n');
sgt = sgtitle(plotTitle,'Color','red');
sgt.FontSize = 20;