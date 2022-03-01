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
