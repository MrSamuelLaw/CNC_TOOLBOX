import QtQuick 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import Qt.labs.platform 1.1

ApplicationWindow {
    id: root
    width: 900
    height: 600
    color: "#29292c"
    visible: true
    title: "CNC-TOOLBOX"

    function parse_tools()
    {
        // send the gcode to the backend & collect the result
        let payload = JSON.stringify({"text": textEditor.text});
        let response = JSON.parse(tool_table_generator.generate(payload));

        if (response.status === true)
        {
            // print the results to the terminal
            var tool_table = response.tool_table
            let lines = tool_table.join("\n");
            terminal.writeToDisplay("The following tools were identified:");
            terminal.writeToDisplay(lines);
            terminal.writeToDisplay("enter y to upload, n to cancel");
        }
        else if (response.status === false)
        {
            // print out the results to the terminal
            terminal.writeToDisplay("Failed with the following errors:");
            terminal.writeToDisplay(response.message);
        }

        // set up the yes and no function for the terminal
        terminal.functionDict["y"] = ()=>{
            let payload = JSON.stringify({"tools": tool_table});
            let response = JSON.parse(tool_table_generator.upload(payload));
            if (response.status === true){
                terminal.writeToDisplay(response.message);
            }
            else {
                terminal.writeToDisplay(response.message);
            }
            delete terminal.functionDict["y"];
            delete terminal.functionDict["n"];
            terminal.endFunction();
        }
        terminal.functionDict["n"] = ()=>{
            terminal.writeToDisplay("upload cancled")
            delete terminal.functionDict["y"];
            delete terminal.functionDict["n"];
            terminal.endFunction();
        }
        terminal.endFunction()

    }

    FileDialog {
        id: fileDialog
        property var func: null
        onAccepted: {func(); terminal.endFunction();}
        onRejected: {
            terminal.writeToDisplay("no file selected");
            terminal.endFunction();
        }

        function import_file(){
            let [type, url] = String(fileDialog.file).split("///");  // collect the type and url
            try {
                terminal.writeToDisplay(`importing from ${url}`);     // display to terminal
                let str = String(filehandler.read_text_file(url));  // request the text from backend
                textEditor.text = str;                              // set text to textArea
            }
            catch(error){
                terminal.writeToDisplay(error); // write any errors to terminal
            }

        }

        function export_file(){
            let [type, url] = String(fileDialog.file).split("///");  // collect the type and url
            let str = textEditor.text;                               // set text to textArea
            try {
                filehandler.write_text_file(url, str);        // request the text be written using backend
                terminal.writeToDisplay(`exporting to ${url}`);  // display to terminal
            }
            catch(error){
                terminal.writeToDisplay(error); // write any errors to terminal
            }
        }

        function run_import_dialog(){
            fileDialog.func = fileDialog.import_file;  // set the function
            fileDialog.fileMode = FileDialog.OpenFile  // open a single file at a time
            fileDialog.acceptLabel = "Import";         // say import next to cancel
            fileDialog.open();                         // run the dialog
        }

        function run_export_dialog(){
            fileDialog.func = fileDialog.export_file;  // set the function
            fileDialog.fileMode = FileDialog.SaveFile  // open a single file at a time
            fileDialog.acceptLabel = "Export";         // say import next to cancel
            fileDialog.open();                         // run the dialog
        }
    }

    Rectangle {
        id: hud
        height: 50
        color: "#3c3c43"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0

        RowLayout {
            id: rowLayout
            anchors.fill: parent
            spacing: 7
            anchors.rightMargin: 10
            anchors.leftMargin: 10


            Button {
                id: importButton
                width: 75
                height: 40
                Layout.minimumWidth: 100
                highlighted: false
                Layout.bottomMargin: 0
                Layout.topMargin: 0
                Layout.fillHeight: true
                hoverEnabled: true
                contentItem: Text {
                    text: "IMPORT"
                    color: "#ffffff"
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle{
                    color: "#00000000"
                    radius: 0
                    border.width: 0
                    anchors.fill: parent
                }
                onHoveredChanged: hovered ?
                                  background.color = "#cc000000":
                                  background.color = "#00000000";

                onClicked: {
                    let cmd = "import";
                    terminal.writeToDisplay(cmd, false);
                    terminal.startFunction();
                }

            }

            Button {
                id: parseToolButton
                width: 75
                height: 40
                Layout.minimumWidth: 100
                Layout.bottomMargin: 0
                Layout.topMargin: 0
                Layout.fillHeight: true
                contentItem: Text {
                    text: "PARSE TOOLS"
                    color: "#ffffff"
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle{
                    color: "#00000000"
                    radius: 0
                    border.width: 0
                    anchors.fill: parent
                }
                onHoveredChanged: hovered ?
                                  background.color = "#cc000000":
                                  background.color = "#00000000"
                onClicked: {
                    let cmd = "parse_tools";
                    terminal.writeToDisplay(cmd, false);
                    terminal.startFunction();
                }

            }

            Button {
                id: exportButton
                width: 75
                height: 40
                Layout.minimumWidth: 100
                contentItem: Text {
                    color: "#ffffff"
                    text: "EXPORT"
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#00000000"
                    radius: 0
                    border.width: 0
                    anchors.fill: parent
                }
                Layout.fillHeight: true
                Layout.bottomMargin: 0
                Layout.topMargin: 0
                onHoveredChanged: hovered ?
                                  background.color = "#cc000000":
                                  background.color = "#00000000";
                onClicked: {
                    let cmd = "export";
                    terminal.writeToDisplay(cmd, false);
                    terminal.startFunction();
                }


            }

            Item {
                id: horizontalSpacer
                width: 200
                height: 200
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }

    TextEditor {
        id: textEditor
        anchors.top: hud.bottom
        anchors.bottom: terminal.top
        anchors.bottomMargin: 0
        anchors.left: parent.left
        anchors.right: parent.right
    }

    Terminal {
        id: terminal
        objectName: "terminalDisplay"  // needed to expose qml to Python
        y: 382
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        Component.onCompleted: {
            terminal.functionDict["import"] = fileDialog.run_import_dialog;
            terminal.functionDict["export"] = fileDialog.run_export_dialog;
            terminal.functionDict["clear_text_editor"] = ()=>{textEditor.text = ""; terminal.endFunction();}
            terminal.functionDict["parse_tools"] = root.parse_tools;
        }
    }

}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.9}D{i:18}
}
##^##*/
