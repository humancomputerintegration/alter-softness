def calculate_speed(pid_output):
    if pid_output < 0:
        speed = int(-49 / 40 * pid_output + 10)
    else:
        speed = int(49 / 40 * pid_output + 10)
    if speed < 0:
        speed = 0
    if speed > 255:
        speed = 255

    speed = speed / 255

    return speed
