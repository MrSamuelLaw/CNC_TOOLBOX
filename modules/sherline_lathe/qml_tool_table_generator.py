import json
from pathlib import Path
from typing import Union
from pydantic import BaseModel
from pydantic.main import Extra
from PySide6.QtCore import QObject
from modules.common.models import Response
from modules.common.decorators import PydanticSlot
from modules.sherline_lathe import tool_table_generator as ttg


class GCode(BaseModel, extra=Extra.forbid):
    text: str


class ToolTable(BaseModel, extra=Extra.forbid):
    tools: list[str]


class ToolTableResponse(Response):
    tool_table: Union[list, None]


class QMLToolTableGenerator(QObject):
    """Bridge between the tool_table_generator module
    and the qml front end."""

    def __init__(self):
        super().__init__()

    @PydanticSlot(model=GCode)
    def generate(self, payload: GCode) -> Response:
        """Generates a tool table from gcode
        text."""

        try:
            tool_table = ttg.generate(payload.text)  # generate the tool table
            if not tool_table:
                raise ValueError("No tools found")
        except Exception as e:
            r = ToolTableResponse(status=False,
                                  message=str(e))
        else:
            r = ToolTableResponse(status=True,
                                  message="tool table generated successfully",
                                  tool_table=tool_table)
        return r

    @PydanticSlot(model=ToolTable)
    def upload(self, payload: ToolTable) -> Response:
        """Saves the tool table generated from a gcode file
        to the path specified in the sherlin_lathe config.json
        file. The path must exist, or else a ValueError is raised."""

        try:
            cur_dir = Path(__file__).parent                # locate current directory
            config_path = cur_dir.joinpath("config.json")  # create url for configs from current directory
            configs = json.loads(config_path.read_text())  # read in the json and parse it
            tool_table_path = configs["tool_table_path"]   # extract tool table path from configs
            tool_table_path = Path(tool_table_path)        # create object
            if tool_table_path.exists():
                text = "\n".join(payload.tools)
                tool_table_path.write_text(text, 'utf-8')  # write it out using path object
            else:
                raise ValueError("path for tool table in sherline lathe config file is not valid")
        except Exception as e:
            r = Response(status=False,
                         message=str(e))
        else:
            r = Response(status=True,
                         message="upload successful")
        return r


