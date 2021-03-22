import QtQuick 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import Qt.labs.platform 1.1

ScrollView {
    id: textEditor
    clip: true
    width: 500
    height: 200
    contentHeight: scrollViewContent.height
    property alias text: textArea.text

    Item {
        id: scrollViewContent
        width: textEditor.width
        height: textArea.contentHeight > textEditor.height ?
                    textArea.contentHeight + 50: textEditor.height

        function update_line_numbers(num_lines){
            let num_lines_str = Array.from(Array(num_lines).keys())  // create and array
            numberLine.text = num_lines_str.join("\n");              // set the numberLine
        }

        TextArea {
            id: numberLine
            width: 40
            readOnly: true
            hoverEnabled: false
            color: "#80ffffff"
            text: "0"
            placeholderTextColor: "#ccffffff"
            placeholderText: qsTr("")
            font.pointSize: 11
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.topMargin: 0
            anchors.leftMargin: 0
        }

        TextArea {
            id: textArea
            selectByMouse: true
            width: textEditor.width - numberLine.width
            height: textEditor.height
            color: "#ffffff"
            anchors.left: numberLine.right
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: 0
            anchors.topMargin: 0
            placeholderTextColor: "#ccffffff"
            font.pointSize: 11
            placeholderText: qsTr("")
            onLineCountChanged: {
                // set the line numbers
                scrollViewContent.update_line_numbers(lineCount);
                // scroll with the user as the screen gets bigger
                if (textArea.cursorPosition == textArea.text.length){
                    textEditor.ScrollBar.vertical.position = (1 - textEditor.ScrollBar.vertical.size);
                }
            }
        }

    }




}
