# Temperature Conversion Data-Processing Project

## Overview
This project demonstrates a data-processing system in ROS 2 with two nodes that work together:

1. **Temperature Publisher Node**: Publishes random temperature values in Celsius
2. **Temperature Converter Node**: Subscribes to Celsius temperatures, converts them to Fahrenheit, and logs the results

## How to Run

### Step 1: Source the workspace
```bash
cd /home/maharshii_patel/utm
source install/setup.bash
```

### Step 2: Run the Temperature Publisher (Terminal 1)
```bash
ros2 run robot_controller temperature_publisher
```

You should see output like:
```
[INFO] [temperature_publisher]: Temperature Publisher Node has started.
[INFO] [temperature_publisher]: Publishing temperatures in Celsius on topic: temperature_celsius
[INFO] [temperature_publisher]: Publishing: 25.37°C
[INFO] [temperature_publisher]: Publishing: 18.92°C
```

### Step 3: Run the Temperature Converter (Terminal 2)
Open a new terminal, source the workspace, and run:
```bash
source /home/maharshii_patel/utm/install/setup.bash
ros2 run robot_controller temperature_converter
```

You should see output like:
```
[INFO] [temperature_converter]: Temperature Converter Node has started.
[INFO] [temperature_converter]: Subscribed to topic: temperature_celsius
[INFO] [temperature_converter]: Received: 25.37°C → Converted: 77.67°F
[INFO] [temperature_converter]: Received: 18.92°C → Converted: 66.06°F
```