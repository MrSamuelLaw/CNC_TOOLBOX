import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.2

Window {
    id: window
    width: 680
    height: 460
    title: "File Dialog"
    color: "#4C4C4C"
    visible: true

    // For details on the JSON hooks please view qml_filebrowser.py
    function list_dir(pathObject) {
        // if its a directory
        if (pathObject.is_dir) {
            listModel.clear();                                // clear the old contents
            let files = JSON.parse(fb.dir(pathObject.path));  // read the new contents
            for (let f of files) {      // loop over each item
                listModel.append({      // add item to list model
                    filename_: f.name,               // file name
                    pathObject_: f,                  // left actual object
                    source_: `image://fb/${f.path}`  // get the file logo
                });
            }

        }
    }

    ListView {  // top level container
        id: listView
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: upButton.bottom
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.topMargin: 0

        // infomative header
        header: Label {
            height: 25
            width: listView.width
            text: "file name"
            leftPadding: 30
            verticalAlignment: "AlignVCenter"
            font.italic: true
            visible: true
        }

        // container for the items that go into the listview
        model: ListModel {
            id: listModel
        }

        // template for items that go into the list view
        delegate: Rectangle {
            id: rectangle
            height: 30
            width: listView.width
            color: window.color
            // container for the path object
            property var pathObject: pathObject_

            // symbol to show
            Image {
                id: symbol
                source: source_
                anchors.verticalCenterOffset: 2
                fillMode: Image.PreserveAspectFit
                anchors.leftMargin: 20
                height: parent.height*0.70
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
            }

            // text to show
            Label {
                id: label
                height: parent.height
                text: filename_
                color: "#ffffff"
                verticalAlignment: "AlignVCenter"
                leftPadding: 10
                anchors.top: parent.top
                anchors.left: symbol.right
            }

            // handles hover and click events
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                property string hoverColor: "#767676"
                // these control the hightlights
                onEntered: (e)=> {
                             parent.color = containsMouse ? hoverColor : window.color
                         }
                onExited: (e)=> {
                             parent.color = containsMouse ? hoverColor : window.color
                          }
                // opens directorys
                onDoubleClicked: (e)=> {list_dir(parent.pathObject);}
            }
        }

        Rectangle {
            id: rectangle1
            x: 337
            y: 124
            width: 0
            height: 30
            color: "#ffffff"
        }
    }

    Button {
        id: upButton
        width: 50
        text: qsTr("<-")
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.leftMargin: 0
        height: 30
        onClicked: ()=>{
                       let curdir = JSON.parse(fb.curdir());
                       let parent = JSON.parse(fb.parent(curdir.path));
                       list_dir(parent);
                   }
    }

    ComboBox {
        id: comboBox
        height: upButton.height
        anchors.left: upButton.right
        anchors.right: doButton1.left
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.rightMargin: 0
        anchors.leftMargin: 0
    }

    Button {
        id: doButton1
        width: 50
        height: 30
        text: qsTr("Do")
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 0
        anchors.topMargin: 0
    }

    // defines what to do on startup
    Component.onCompleted: list_dir(JSON.parse(fb.curdir()));

}



