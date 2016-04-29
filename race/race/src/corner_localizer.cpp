#include <ros/ros.h>
#include <race/corner_loc.h>
#include <sensor_msgs/LaserScan.h>
#include <cmath>

#define PI 3.141592

bool cornerServiceCallback(race::corner_loc::Request&, race::corner_loc::Response&);
void laserCallback(const sensor_msgs::LaserScanConstPtr&);

int getRange(const sensor_msgs::LaserScan&, double theta);
int getAngle(const sensor_msgs::LaserScan& data, int index);

sensor_msgs::LaserScan latestLaser;
bool laser_set = false;

int main(int argc, char* argv[]) {
    ros::init(argc, argv, "corner_localizer");
    
    ros::NodeHandle node;
    
    ros::ServiceServer cornerServer = node.advertiseService("corner", cornerServiceCallback);
    ros::Subscriber laserSub = node.subscribe<sensor_msgs::LaserScan>("scan", 10, laserCallback);
    
    ros::spin();
}

bool cornerServiceCallback(race::corner_loc::Request& req, race::corner_loc::Response& res)
{
    ROS_INFO("Obtaining request...");
    if(!laser_set) {
        ROS_INFO("Laser not set!");
        res.found = false;
        return false;
    }
    
    double maxCheck = getRange(latestLaser, 55);
    double minCheck = getRange(latestLaser, 0);
    
    for(int i = maxCheck; i <= (minCheck - 1); i--) {
        if(latestLaser.ranges[i] > latestLaser.ranges[i + 1] * 2) {
            double angle = getAngle(latestLaser, i+1);
            double distance = latestLaser.ranges[i+1];
            res.found = true;
            res.x = distance*sin(angle);
            res.y = distance*cos(angle);
            ROS_INFO("Result returned! Found");
            return true;
        }
    }

   res.found = false;
    
   ROS_INFO("Result returned! Not found");

    return true;
}

void laserCallback(const sensor_msgs::LaserScanConstPtr& msg)
{
    laser_set = true;
    
    latestLaser = *msg;
}


int getRange(const sensor_msgs::LaserScan& data, double theta) {
    theta += 45;
    theta = theta * 2*PI / 360.0;
    double newTheta = data.ranges[(int)((1/data.angle_increment)*theta)];
    if(newTheta > data.angle_max or newTheta < data.angle_min)
        return -1;
    else
        return newTheta;
}

int getAngle(const sensor_msgs::LaserScan& data, int index) {
    return index*data.angle_increment + data.angle_min;
}
