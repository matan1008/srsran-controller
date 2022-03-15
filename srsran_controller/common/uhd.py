import asyncio
import re
from asyncio.subprocess import PIPE, DEVNULL


async def get_available_devices():
    """
    Get all available UHD devices.
    """
    proc = await asyncio.create_subprocess_exec('uhd_find_devices', stdout=PIPE, stderr=DEVNULL)
    await proc.wait()
    devices = (await proc.stdout.read()).decode()
    return [f'serial={d}' for d in re.findall(r'\s*serial: (.*)', devices)]


async def query_sensor(sensor: str, address: str = '') -> str:
    """
    Query a specific device for a sensor, e.g. /mboards/0/sensors/gps_gpgga or /mboards/0/sensors/gps_locked.
    :param sensor: Sensor name, run uhd_usrp_probe for all sensors.
    :param address: Device address filter.
    """
    proc = await asyncio.create_subprocess_exec('uhd_usrp_probe', '--args', address, '--sensor', sensor, stdout=PIPE,
                                                stderr=DEVNULL)
    await proc.wait()
    return (await proc.stdout.read()).decode().strip()
