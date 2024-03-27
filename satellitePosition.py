import math, datetime
import pandas as pd


banner = \
"""
⠀⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡀⠀⠀⠀
⠀⠀⠛⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣿⠛⠀⠀⠀⠀⠀⡀⠺⣿⣿⠟⢀⡀⠀
⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣦⠈⠁⣴⣿⣿⡦
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡈⠻⠟⢁⣴⣦⡈⠻⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡀⠺⣿⣿⠟⢀⡀⠻⣿⡿⠋⠀⠀⠀
⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⡿⠿⣿⣦⡈⠁⣴⣿⣿⡦⠈⠀⠀⠀⠀⠀
⠲⣿⠷⠂⠀⠀⠀⠀⠀⠀⢀⣴⡿⠋⣠⣦⡈⠻⣿⣦⡈⠻⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⡀⠺⣿⣿⣿⡦⠈⣻⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡈⠻⣿⣦⡈⠻⠋⣠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡀⠺⣿⣿⠟⢀⡈⠻⣿⣶⣾⡿⠋⣠⣦⡀⠀⢀⣠⣤⣀⡀⠀⠀
⠀⠀⠀⠀⣠⣾⣿⣦⠈⠁⣴⣿⣿⡦⠈⠛⠋⠀⠀⠈⠛⢁⣴⣿⣿⡿⠋⠀⠀⠀
⠀⠀⣠⣦⡈⠻⠟⢁⣴⣦⡈⠻⠋⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣏⠀⠀⠀⠀⠀
⠀⠺⣿⣿⠟⢀⡀⠻⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⡿⠛⠁⠙⣷⣶⣦⠀⠀
⠀⠀⠈⠁⣴⣿⣿⡦⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠻⠿⠟⠀   
     ⠈⠻⠋                    
     
 _____       _       _ _ _ _      ______         _ _   _             
/  ___|     | |     | | (_) |     | ___ \       (_) | (_)            
\ `--.  __ _| |_ ___| | |_| |_ ___| |_/ /__  ___ _| |_ _  ___  _ __  
 `--. \/ _` | __/ _ \ | | | __/ _ \  __/ _ \/ __| | __| |/ _ \| '_ \ 
/\__/ / (_| | ||  __/ | | | ||  __/ | | (_) \__ \ | |_| | (_) | | | |
\____/ \__,_|\__\___|_|_|_|\__\___\_|  \___/|___/_|\__|_|\___/|_| |_|
                                                      by Ilias Doukas
"""


def get(df, key):
    """ Dataframe getter """
    return(df[df['key'] == key]['value'].values[0])

def arctan(num, den):
    if den != 0:
        angle = math.atan(num / den)
        if num > 0 and den < 0 or num < 0 and den < 0: 
            angle = math.pi + angle
        elif num < 0 and den > 0:
            angle = 2 * math.pi + angle
        elif num == 0 and den >= 0:
            angle = 0
        elif num == 0 and den < 0:
            angle = math.pi
    elif den == 0 and num > 0:
        angle = math.pi / 2
    elif den == 0 and num < 0:
        angle = 3 * math.pi / 2
    if angle > 2 * math.pi:
        k = angle // (2 * math.pi)
        angle -= k * 2 * math.pi
    return(angle)



def satellite_position(filename, target_time_str):
    """ Calculates satellite position at WGS84 (X, Y, Z) 
    based on navigation & orbit data (brdc file) at a given time

    args: 
    -filename: rinex v3.04 navigation file as csv
    -target_time_str: target time, format "%Y-%m-%d %H:%M:%S"

    returns:
    X, Y, Z coordinates of satellite's position
    """

    print(banner)

    # Navigation message & orbit data
    df = pd.read_csv(filename)
    df['value'][1:] = df['value'][1:].astype("float64")

    # Constants
    _pi = math.pi
    _m = 3.986005e14
    omega_dot_e = 7.2921151467e-5

    # Megalos hmiaksonas A
    axis_A = get(df, "sqrt_a")**2

    # Prosdiorismeni mesi kinhsh
    _n0 = math.sqrt(_m / axis_A**3)

    # Target time str to UNIX timestamp (seconds)
    target_time = datetime.datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S") .timestamp()

    # TOE to UNIX timestamp (seconds)
    toe_timestamp = datetime.datetime(int(get(df, "year")), int(get(df, "month")), int(get(df, "day")), 
                                      int(get(df, "hour")), int(get(df, "minute")), int(get(df, "second"))).timestamp()

    # Xronikh diafora apo xrono anaforas efhmeridas
    _tk = target_time - toe_timestamp

    # Diorthomeni mesh kinhsh
    _n = _n0 + get(df, "dn")

    # Mesh anwmalia
    _Mk = get(df, "Mo") + _n * _tk

    # Ekkentrh anwmalia
    # Newton - Raphson
    er = 10**-6
    iters = 0
    _Ek0 = _Mk

    while True:
        _Ek = _Ek0 - (_Ek0 - get(df, "eccentr") * math.sin(_Ek0) - _Mk) / (1 - get(df, "eccentr") * math.cos(_Ek0))
        
        iters += 1
        if abs(_Ek - _Ek0) < er: break

        _Ek0 = _Ek

    if _Ek < 0: _Ek += 2 * _pi
    
    # iters 2
    # 3.0924923831837314

    # Alithis anwmalia
    num = math.sqrt(1 - get(df, "eccentr")**2) * math.sin(_Ek) / (1 - get(df, "eccentr") * math.cos(_Ek))
    den = (math.cos(_Ek) - get(df, "eccentr")) / (1 - get(df, "eccentr") * math.cos(_Ek))
    _vk = arctan(num, den)

    # Elegxos Ek
    _Ek_ = math.acos((get(df, "eccentr") + math.cos(_vk)) / (1 + get(df, "eccentr") * math.cos(_vk)))
    # 3.092492383183731

    # Orisma platous
    _Fk = _vk + get(df, "omega_")

    # Parelkseis
    _duk = get(df, "cus") * math.sin(2 * _Fk) + get(df, "cuc") * math.cos(2 * _Fk)
    _drk = get(df, "crs") * math.sin(2 * _Fk) + get(df, "crc") * math.cos(2 * _Fk)
    _dik = get(df, "cis") * math.sin(2 * _Fk) + get(df, "cic") * math.cos(2 * _Fk)

    # Diorthomeno orisma tou platous
    _uk = _Fk + _duk

    # Diorthomenh aktina
    _rk = axis_A * (1 - get(df, "eccentr") * math.cos(_Ek)) + _drk

    # Diorthomenh gwnia klishs
    _ik = get(df, "Io") + _dik + get(df, "idot") * _tk

    # Syntetagmenes doryforou sto troxiako epipedo
    _xk_p = _rk * math.cos(_uk)
    _yk_p = _rk * math.sin(_uk)

    # Diorthomenh orthi anafora aniontos desmou
    omega_k = get(df, "OMEGA") + (get(df, "OMEGA_dot") - omega_dot_e) * _tk - omega_dot_e * get(df, "toe")

    # Syntetagmenes doryforou sto WGS84
    _xk = _xk_p * math.cos(omega_k) - _yk_p * math.cos(_ik) * math.sin(omega_k)
    _yk = _xk_p * math.sin(omega_k) + _yk_p * math.cos(_ik) * math.cos(omega_k)
    _zk = _yk_p * math.sin(_ik)

    print(f"• Satellite  🛰 ({get(df, 'gps')}) position at {target_time_str} →")
    print(f"X: {round(_xk, 3)}m ")
    print(f"Y: {round(_yk, 3)}m ")
    print(f"Z: {round(_zk, 3)}m ")
    return(round(_xk, 3), round(_yk, 3), round(_zk, 3))



# • Satellite  🛰 (G01) position at 2022-07-21 17:24:30 →
# X: 15498762.112m 
# Y: 13411622.34m 
# Z: -17390320.311m 

# • Satellite  🛰 (G01) position at 2022-07-21 18:00:00 →
# X: 10469863.268m 
# Y: 13364766.271m 
# Z: -20825889.823m 

target_time_str = "2022-07-21 17:24:30"
# target_time_str = "2022-07-21 18:00:00"
x, y, z = satellite_position("data.csv", target_time_str)


# *  2022  7 21 18  0  0.00000000
# PG01  10469.863444  13364.767433 -20825.890640
x_sp3 = 10469.863444 * 1000
y_sp3 = 13364.767433 * 1000
z_sp3 = -20825.890640 * 1000

dx = round(x - x_sp3, 3)
dy = round(y - y_sp3, 3)
dz = round(z - z_sp3, 3)
# print(dx, dy, dz)
# -0.176 -1.162 0.817

