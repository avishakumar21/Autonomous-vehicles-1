vehicle_ID = 8;
len    = length(per_vehicle{vehicle_ID});

% Raw acceleration
y         = per_vehicle{vehicle_ID}(:,3);

% Raw speed & thresholds
speed     = zeros(len, 1);
threshold = zeros(len, 1);

% Build erratic acceleration thresholds from speed
for i = 1:len
    x_vel = per_vehicle{vehicle_ID}(i,4);
    y_vel = per_vehicle{vehicle_ID}(i,5);
    cur_speed = sqrt(x_vel^2 + y_vel^2);
    if(cur_speed<=40)
        threshold(i) = 200;
    elseif(cur_speed<=60)
        threshold(i) = 180;
    elseif(cur_speed<=80)
        threshold(i) = 160;
    elseif(cur_speed<=100)
        threshold(i) = 140;
    elseif(cur_speed<=120)
        threshold(i) = 120;
    else
        threshold(i) = .100;
    end
end

% Low Pass Filter (LPF) using Exponential Moving Average (EMA)
movAvg = dsp.MovingAverage('Method','Exponential weighting','ForgettingFactor',0.5);
y_f    = movAvg(y);

% Gradient of Acceleration = Jerk
y_fd   = zeros(len, 1);
Ts     = 0.1;
y_fd(1)= y_f(1);
for i = 2:len
    y_fd(i) = (y_f(i) - y_f(i-1)) / Ts;
end

% Jerk samples are summed over a moving window 
%   Identifies high concentrations of acceleration, which indicate a 
%   lateral or longitudinal driving event
N = 20;
y_fds = movsum(y_fd, N);

figure
plot(y_fd)

figure
plot(y_fds)
hold on
plot(threshold)