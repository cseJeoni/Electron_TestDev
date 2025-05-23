def generate_servo_mode_command(target_position):
    return _generate_mode_command(mode_code=0x01, speed=0, position=target_position, force=0)

def generate_position_mode_command(target_position):
    return _generate_mode_command(mode_code=0x00, speed=0, position=target_position, force=0)

def generate_speed_mode_command(target_speed, target_position):
    return _generate_mode_command(mode_code=0x02, speed=target_speed, position=target_position, force=0)

def generate_speed_force_mode_command(target_force, target_speed, target_position):
    return _generate_mode_command(mode_code=0x05, speed=target_speed, position=target_position, force=target_force)

def generate_force_mode_command(target_force):
    # target_force는 g 단위 (예: 1000g = 0x03E8)
    header = [0x55, 0xAA]
    frame_length = 0x09
    motor_id = 0x01
    command_type = 0x32

    control_mode_register = [0x25, 0x00]
    control_mode_setting = [0x03, 0x00]  # 0x03: force mode
    not_used = [0x00, 0x00]
    force_data = [target_force & 0xFF, (target_force >> 8) & 0xFF]

    payload = control_mode_register + control_mode_setting + not_used + force_data
    checksum = (frame_length + motor_id + command_type + sum(payload)) & 0xFF

    return bytes(header + [frame_length, motor_id, command_type] + payload + [checksum])

def _generate_mode_command(mode_code, speed, position, force, frame_length=0x0D):
    header = [0x55, 0xAA]
    motor_id = 0x01
    command_type = 0x32

    control_mode_register = [0x25, 0x00]
    control_mode_setting = [mode_code, 0x00]
    not_used = [0x00, 0x00]

    force_data = [force & 0xFF, (force >> 8) & 0xFF]
    speed_data = [speed & 0xFF, (speed >> 8) & 0xFF]
    position_data = [position & 0xFF, (position >> 8) & 0xFF]

    payload = (
        control_mode_register + control_mode_setting + not_used +
        force_data + speed_data + position_data
    )

    checksum = (frame_length + motor_id + command_type + sum(payload)) & 0xFF

    return bytes(header + [frame_length, motor_id, command_type] + payload + [checksum])
