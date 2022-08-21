import asyncio
from json import loads
from pathlib import Path
from typing import Dict

import psutil
from aiohttp import ClientSession
from discord import Color, Embed, Webhook

CHECK_INTERVAL_S = 60

# TODO: don't hardcode these, make configurable
PATH_USED_DISK_SPACE_C = "C:/"
PATH_USED_DISK_SPACE_I = "I:/"
PATH_USED_DISK_SPACE_J = "J:/"

CPU_PERC_CRIT = 90.0
VMEM_PERC_CRIT = 85.0
DISK_C_CRIT = 70.0
DISK_I_CRIT = 95.0
DISK_J_CRIT = 95.0
TAKE_ACTION_MSG = "Take action now. This alarm will repeat until resolved."
config: Dict[str, str] = loads(Path("config.json").read_text())


def format_desc_msg(
    device_name: str, current_value: float | str, crit_value: float | str
) -> str:
    return f"{device_name} usage ({str(current_value)}%) from last {CHECK_INTERVAL_S}s greater than critical limit ({str(crit_value)}%). {TAKE_ACTION_MSG}"


def format_title_msg(device_name: str) -> str:
    return f"{device_name} Usage Critical!"


async def main():

    async with ClientSession() as session:
        webhook = Webhook.from_url(url=config["webhook_url"], session=session)

        while True:
            cpu_perc = psutil.cpu_percent(interval=None)
            vmem_perc = psutil.virtual_memory().percent
            disk_space_C_perc = psutil.disk_usage(PATH_USED_DISK_SPACE_C).percent
            disk_space_I_perc = psutil.disk_usage(PATH_USED_DISK_SPACE_I).percent
            disk_space_J_perc = psutil.disk_usage(PATH_USED_DISK_SPACE_J).percent

            # TODO: this can be done without so many "if"s?
            if cpu_perc >= CPU_PERC_CRIT:
                await webhook.send(
                    embed=Embed(
                        title=format_title_msg("CPU"),
                        description=format_desc_msg("CPU", cpu_perc, CPU_PERC_CRIT),
                        color=Color.red(),
                    )
                )
            if vmem_perc >= VMEM_PERC_CRIT:
                await webhook.send(
                    embed=Embed(
                        title=format_title_msg("Memory"),
                        description=format_desc_msg(
                            "Memory", vmem_perc, VMEM_PERC_CRIT
                        ),
                        color=Color.red(),
                    )
                )
            if disk_space_C_perc >= DISK_C_CRIT:
                await webhook.send(
                    embed=Embed(
                        title=format_title_msg("Disk C:"),
                        description=format_desc_msg(
                            "Disk C:", disk_space_C_perc, DISK_C_CRIT
                        ),
                        color=Color.red(),
                    )
                )
            if disk_space_I_perc >= DISK_I_CRIT:
                await webhook.send(
                    embed=Embed(
                        title=format_title_msg("Disk I:"),
                        description=format_desc_msg(
                            "Disk I:", disk_space_I_perc, DISK_I_CRIT
                        ),
                        color=Color.red(),
                    )
                )
            if disk_space_J_perc >= DISK_J_CRIT:
                await webhook.send(
                    embed=Embed(
                        title=format_title_msg("Disk J:"),
                        description=format_desc_msg(
                            "Disk J:", disk_space_J_perc, DISK_J_CRIT
                        ),
                        color=Color.red(),
                    )
                )

            await asyncio.sleep(CHECK_INTERVAL_S)


if __name__ == "__main__":
    asyncio.run(main())
