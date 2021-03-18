import json
from pathlib import Path
from typing import Union
from pydantic import BaseModel
from pydantic.main import Extra
from PySide6.QtCore import QObject, Slot
from modules.sherline_lathe import tool_table_generator as ttg


class GCode(BaseModel, extra=Extra.forbid):
    text: str


class ToolTable(BaseModel, extra=Extra.forbid):
    tools: list[str]


class Response(BaseModel):
    status: bool
    message: str
    tool_table: Union[list, None]


class QMLToolTableGenerator(QObject):
    """Bridge between the tool_table_generator module
    and the qml front end."""

    def __init__(self):
        super().__init__()

    @Slot(str, result=str)
    def generate(self, payload: str) -> str:
        """Generates a tool table from gcode
        text."""

        try:
            gcode = GCode.parse_raw(payload)       # validate payload
            tool_table = ttg.generate(gcode.text)  # generate the tool table
        except Exception as e:
            r = Response(status=False,
                         message=str(e))
        else:
            r = Response(status=True,
                         message="tool table generated successfully",
                         tool_table=tool_table)
        return r.json()


    @Slot(str, result=str)
    def upload(self, payload: str) -> str:
        """Saves the tool table generated from a gcode file
        to the path specified in the sherlin_lathe config.json
        file. The path must exist, or else a ValueError is raised."""

        try:
            tool_table = ToolTable.parse_raw(payload)      # validate payload
            cur_dir = Path(__file__).parent                # locate current directory
            config_path = cur_dir.joinpath("config.json")  # create url for configs from current directory
            configs = json.loads(config_path.read_text())  # read in the json and parse it
            tool_table_path = configs["tool_table_path"]   # extract tool table path from configs
            tool_table_path = Path(tool_table_path)        # create object
            if tool_table_path.exists():
                text = "\n".join(tool_table.tools)
                tool_table_path.write_text(text, 'utf-8')  # write it out using path object
            else:
                raise ValueError("path for tool table in sherline lathe config file is not valid")
        except Exception as e:
            r = Response(status=False,
                         message=str(e))
        else:
            r = Response(status=True,
                         message="upload successful")
        return r.json()


