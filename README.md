# satellitePosition
This tool calculates satellite position at WGS84 (X, Y, Z) based on navigation & orbit data (brdc file) at a given time.

## Requirements:
python >= 3.10 and pandas

## args: 
-**filename**: rinex v3.04 navigation file as csv    
-**target_time_str**: target time, format "%Y-%m-%d %H:%M:%S"

## returns:
X, Y, Z coordinates of satellite's position
