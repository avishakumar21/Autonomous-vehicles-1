%{
    ECE 6680 - Final Project
    @author Tyler S. Sherman
    @date 04.27.2020
    @version 01
%}
%*************************************************************************%
%                             IMPORT & REFORMAT                           %
%*************************************************************************%
collisions_per_sim = zeros(1, 9);
speed_per_sim = {1, 9};
headway_per_sim = {1, 9};
accel_per_sim = {1, 9};

files = {'../Data/avAnimal.csv', '../Data/avEMS(2).csv', '../Data/avPothole.csv', '../Data/humanAnimal.csv', '../Data/humanEMS.csv', '../Data/humanPothole.csv', '../Data/noV2VAnimal.csv', '../Data/noV2VEMS.csv', '../Data/noV2VPothole.csv'};
for file_number = 1:length(files)
    % Import Data from CSV
    % COLUMNS = time,   ID,  accel,  vel,   pos,  collisions
    M = readtable(char(files(1, file_number)));
    M_height = height(M);

    % Time properties
    t_full = table2array(M(:,1));
    for t = 1:length(t_full)
        t_full(t) = round(t_full(t), 1, 'decimal');
    end
    t_unique = unique(t_full, 'stable');
    cycles   = length(t_unique);
    t_start  = 0.0;
    t_end    = t_unique(cycles);
    counts   = histc(t_full, t_unique);

    % ID properties
    ID_full     = table2array(M(:,2));
    ID_unique   = unique(ID_full, 'stable');
    numVehicles = length(ID_unique);

    % Acceleration properties
    a = table2array(M(:,3));

    % Velocity properties
    vel = table2array(M(:,4));
    x_vel = zeros(length(vel), 1);
    y_vel = zeros(length(vel), 1);
    for i = 1:length(vel)
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

    % Position properties
    pos = table2array(M(:,5));
    x_pos = zeros(length(pos), 1);
    y_pos = zeros(length(pos), 1);
    for i = 1:length(pos)
        temp_pos = pos{i};
        temp_split = split(temp_pos, ["(",","," ",")"]);
        x_pos(i) = str2double(temp_split{2});
        y_pos(i) = str2double(temp_split{4});
    end

    % Collisions
    collisions = table2array(M(:,6));
    collisions_per_sim(file_number) = max(collisions);
    %fprintf('There were %u collisions in this simulation\n', num_collisions);

    % Recombine data into matrix
    % COLUMNS = time, ID, accel, x-vel, y-vel, x-pos, y-pos, lane
    Data = [t_full, ID_full, a, x_vel, y_vel, x_pos, y_pos, y_pos];
    lane_cords = [0 60 65 70 100];
    for val = 1:length(Data)
        lane = find(Data(val,7)<=lane_cords, 1, 'first') - 1;
        Data(val, 8) = lane;
    end

    
%*************************************************************************%
%                          PER VEHICLE STATISTICS                         %
%*************************************************************************%
    max_ID = max(ID_unique);
    per_vehicle = cell(max_ID, 1);

    for val = 1:length(Data)
        cur_row = Data(val, :);
        cur_ID = cur_row(2);
        per_vehicle{cur_ID, 1} = [per_vehicle{cur_ID, 1}; cur_row];
    end

    % Calculate average speeds (x-direction)
    avg_speed_array = zeros(numVehicles, 1);
    avg_accel_array = zeros(numVehicles, 1);
    for i = 1:numVehicles
        ID = ID_unique(i);
        avg_speed_meters = mean(sqrt(per_vehicle{ID, 1}(:, 4).^2 + per_vehicle{ID, 1}(:, 5).^2));
        avg_accel_meters = mean(per_vehicle{ID, 1}(:, 3));
        avg_speed_miles = avg_speed_meters*2.236936;
        %fprintf('Vehicle %u has an average speed of %.2f m/s (%.2f mph)\n', ID, avg_speed_meters, avg_speed_miles)
        avg_speed_array(i) = avg_speed_meters;
        avg_accel_array(i) = avg_accel_meters;
    end
    speed_per_sim{file_number} = avg_speed_array;
    accel_per_sim{file_number} = avg_accel_array;

    % Use erratic driving algorithm to classify behavior


    
%*************************************************************************%
%                      VEHICLE HEADWAY CATEGORIZATION                     %
%*************************************************************************%
    index = 1;
    headway_counter = zeros(4, 1); % one bin for each headway type
    car_size = 4.5;
    % Go through each time step
    for i = 1:cycles
        cur_time = t_unique(i);
        num_vehicles_present = counts(i);

        % First vehicle at index
        % Last vehicle at index+num_vehicles_present

        % For each vehicle:
        %    find closest vehicle in front of it in same lane
        for j = 0:num_vehicles_present-1
            cur_vehicle = Data(index+j, :);
            distance = intmax; %arbitrary large number
            for k = 0:num_vehicles_present-1
                tmp_vehicle = Data(index+k, :);

                % Want:
                %    Different IDs
                %    Same lane
                %    cur_vehicle to be the trailing vehicle
                if(cur_vehicle(2)~=tmp_vehicle(2) && cur_vehicle(8)==tmp_vehicle(8) && cur_vehicle(6)>tmp_vehicle(6))
                    distance_new = cur_vehicle(6) - tmp_vehicle(6) + car_size;
                    % Only want the closest vehicle
                    if(distance_new < distance)
                        distance = distance_new;
                    end
                end

            end
            if(distance < intmax) % there was a front vehicle found
                % headway =  range between two vehicles divided by speed of the following vehicle
                headway = distance/abs(cur_vehicle(4));
                if(headway <= 0.6)                      % Danger Zone
                    headway_counter(1) = headway_counter(1) + 1; 
                elseif(headway > 0.6 && headway <= 1.0) % Critical Zone
                    headway_counter(2) = headway_counter(2) + 1; 
                elseif(headway > 1.0 && headway <= 1.7) % Normal Zone
                    headway_counter(3) = headway_counter(3) + 1; 
                else                                    % Pursuit Zone
                    headway_counter(4) = headway_counter(4) + 1; 
                end
                % categorize the headway
            end
        end

        % Increment index for next time step
        index = index+num_vehicles_present;
    end
    headway_per_sim{file_number} = headway_counter; 
end
clearvars -except collisions_per_sim speed_per_sim headway_per_sim accel_per_sim
%% PLOTTING COLLISIONS
figure
y = [collisions_per_sim(1), collisions_per_sim(4), collisions_per_sim(7); collisions_per_sim(2), collisions_per_sim(5), collisions_per_sim(8); collisions_per_sim(3), collisions_per_sim(6), collisions_per_sim(9)];
bar(y);
% Plot Properties
title('Total Number of Collisions Per Simulation')
set(gca,'xticklabel',{'Animal Crossing Scenario','EMS Scenario','Pothole Scenario'});
xlabel('Simulation Type')
ylabel('Number of Collisions')
grid on
legend('AV with V2V', 'Human', 'AV no V2V', 'location', 'northwest');

%% PLOTTING VEHICLE SPEEDS
% Sub-plot 1: Animal Crossing Scenario 
figure
subplot(1,3,1)
%sgtitle('Vehicle Speeds');
V2V   = [speed_per_sim{1}];
H     = [speed_per_sim{4}];
AV    = [speed_per_sim{7}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Animal Crossing Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Speed (m/s)')

% Sub-plot 2: EMS Scenario
subplot(1,3,2)
V2V   = [speed_per_sim{2}];
H     = [speed_per_sim{5}];
AV    = [speed_per_sim{8}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('EMS Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Speed (m/s)')

% Sub-plot 3: Pothole Scenario
subplot(1,3,3)
V2V   = [speed_per_sim{3}];
H     = [speed_per_sim{6}];
AV    = [speed_per_sim{9}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Pothole Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Speed (m/s)')

%% PLOTTING VEHICLE ACCELERATIONS
% Sub-plot 1: Animal Crossing Scenario 
figure
subplot(1,3,1)
%sgtitle('Vehicle Accelerations');
V2V   = [accel_per_sim{1}];
H     = [accel_per_sim{4}];
AV    = [accel_per_sim{7}];
group = [ones(size(V2V)); 2*ones(size(H)); 3*ones(size(AV))];
boxplot([V2V; H; AV], group)
% Plot Properties
title('Animal Crossing Scenario')
set(gca,'XTickLabel',{'AV with V2V','Human','AV no V2V'})
xlabel('Vehicle Type')
ylabel('Acceleration (m/s^2)')

% Sub-plot 2: EMS Scenario
subplot(1,3,2)
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
subplot(1,3,3)
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

%% PLOTTING VEHICLE HEADWAY
% Sub-plot 1: Animal Crossing Scenario 
figure
subplot(3,1,1)
%sgtitle('Vehicle Headway Classification');
V2V = [headway_per_sim{1}];
H   = [headway_per_sim{4}];
AV  = [headway_per_sim{7}];
y   = [V2V(1), H(1), AV(1); V2V(2), H(2), AV(2); V2V(3), H(3), AV(3); V2V(4), H(4), AV(4)];
bar(y);
% Plot Properties
title('Animal Crossing')
set(gca,'xticklabel',{'Danger','Critical','Normal','Pursuit'});
xlabel('Headway Categorization Zone')
ylabel('Number of Instances')
grid on
legend('AV with V2V', 'Human', 'AV without V2V', 'location', 'best');

% Sub-plot 2: EMS Scenario
subplot(3,1,2)
V2V = [headway_per_sim{2}];
H   = [headway_per_sim{5}];
AV  = [headway_per_sim{8}];
y   = [V2V(1), H(1), AV(1); V2V(2), H(2), AV(2); V2V(3), H(3), AV(3); V2V(4), H(4), AV(4)];
bar(y);
% Plot Properties
title('Emergency Responder')
set(gca,'xticklabel',{'Danger','Critical','Normal','Pursuit'});
xlabel('Headway Categorization Zone')
ylabel('Number of Instances')
grid on
legend('AV with V2V', 'Human', 'AV without V2V', 'location', 'best');

% Sub-plot 3: Pothole Scenario 
subplot(3,1,3)
V2V = [headway_per_sim{3}];
H   = [headway_per_sim{6}];
AV  = [headway_per_sim{9}];
y   = [V2V(1), H(1), AV(1); V2V(2), H(2), AV(2); V2V(3), H(3), AV(3); V2V(4), H(4), AV(4)];
bar(y);
% Plot Properties
title('Pothole')
set(gca,'xticklabel',{'Danger','Critical','Normal','Pursuit'});
xlabel('Headway Categorization Zone')
ylabel('Number of Instances')
grid on
legend('AV with V2V', 'Human', 'AV without V2V', 'location', 'best');
