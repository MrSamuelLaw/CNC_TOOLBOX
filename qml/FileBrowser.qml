import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.2
import QtQuick.Layouts 1.11

Window {
    id: root
    title: "File Dialog"
    color: "#4C4C4C"
    visible: true
    width: 600
    height: 400

    //    ______                _   _
    //   |  ____|              | | (_)
    //   | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
    //   |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
    //   | |  | |_| | | | | (__| |_| | (_) | | | \__ \
    //   |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/


    // For details on the JSON hooks please view qml_filebrowser.py
    function list_dir(pathObject) {
        // if its a directory
        if (pathObject.is_dir) {
            // update the heading location
            breadCrumbText.text = pathObject.path
            // clear the old contents
            listModel.clear();
            // read the new contents
            let files = JSON.parse(fb.dir(pathObject.path));
            // loop over each item
            for (let f of files) {
                // add item to list model
                listModel.append({
                                     filename_: f.name,                 // file name
                                     pathObject_: f,                    // left actual object
                                     source_: `image://fb/${f.path}`,   // get the file logo
                                     suffix_: f.suffix ? f.suffix :     // file type
                                                         f.is_dir ? "dir" :
                                                                    f.is_file ? f.name :
                                                                                "file",
                                     timestamp_: f.seconds              // timestamp
                                 });
            }

        }
    }

    function sort_by_name() {
        // get all the names
        let names = [];
        for (let i = 0; i < listModel.count; i++){
            let n = listModel.get(i).pathObject_.name;
            names.push(n);
        }
        // sort the names
        names.sort((a, b)=>a.localeCompare(b));
        // create helper function
        let index_from_name = function(name){
            for (let i = 0; i < listModel.count; i++){
                if (name === listModel.get(i).pathObject_.name){
                    return i;
                }
            }
        }
        // apply the sort
        for (let i = 0; i < names.length; i++){
            listModel.move(index_from_name(names[i]), i, 1);
        }


    }

    //    _____ _
    //   |_   _| |
    //     | | | |_ ___ _ __ ___  ___
    //     | | | __/ _ \ '_ ` _ \/ __|
    //    _| |_| ||  __/ | | | | \__ \
    //   |_____|\__\___|_| |_| |_|___/

    RowLayout {
        id: navRibbon
        height: 35
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 1
        spacing: 1

        Button {
            id: upButton
            text: "<-"
            Layout.preferredHeight: 0
            Layout.fillHeight: true
            Layout.preferredWidth: 75
            onClicked: ()=>{
                           let curdir = JSON.parse(fb.curdir());
                           let parent = JSON.parse(fb.parent(curdir.path));
                           list_dir(parent);
                       }
        }

        Rectangle {
            id: breadCrumbRect
            Layout.fillHeight: true
            Layout.fillWidth: true
            Text {
                id: breadCrumbText
                text: qsTr("C://current/path")
                anchors.fill: parent
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
                leftPadding: 10
            }
        }

        ComboBox {
            id: filter
            Layout.fillHeight: true
            Layout.preferredWidth: 99
            displayText: "filters"
        }

        Button {
            id: doButton
            text: "Do"
            Layout.preferredWidth: 75
            Layout.fillHeight: true
            Layout.preferredHeight: 75
        }
    }

    ScrollView {
        id: scrollView
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.top: navRibbon.bottom
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 1
        contentWidth: contentWidth()

        function contentWidth(){
            let content_width = 0;
            // loop over the children items, minus the filler bar
            for(let i = 0; i < listViewRibbon.children.length - 1; i++){
                content_width += listViewRibbon.children[i].width;
            }
            // return root.width if the content width is not wide enough
            return (content_width > root.width) ? content_width : root.width;
        }

        RowLayout {
            id: listViewRibbon
            height: 35
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            spacing: 1
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.topMargin: 0

            Rectangle {
                id: fileTitleRect
                x: 0
                width: 175
                color: "#ffffff"
                Layout.minimumWidth: 175
                Layout.fillHeight: true

                Text {
                    id: fileTitle
                    text: qsTr("File Name")
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.leftMargin: 10
                }

                Text {
                    id: titleSorting
                    text: qsTr("A -> Z")
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 10
                }

                MouseArea {
                    anchors.fill: parent
                    scrollGestureEnabled: false
                    hoverEnabled: true
                    onEntered: ()=>{parent.color = "#727272";}
                    onExited: ()=>{parent.color = "#ffffff";}
                    onClicked: sort_by_name();
                }
            }

            Rectangle {
                id: fileDateRect
                x: 0
                width: 175
                color: "#ffffff"
                Layout.minimumWidth: 175
                Layout.fillHeight: true
                Text {
                    id: dateTitle
                    text: qsTr("Date Modified")
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.leftMargin: 10
                }

                Text {
                    id: dateSorting
                    text: qsTr("New -> Old")
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 10
                }

                MouseArea {
                    anchors.fill: parent
                    scrollGestureEnabled: false
                    hoverEnabled: true
                    onEntered: ()=>{parent.color = "#727272";}
                    onExited: ()=>{parent.color = "#ffffff";}
                }
            }

            Rectangle {
                id: fileTypeRect
                x: 0
                width: 175
                color: "#ffffff"
                Layout.minimumWidth: 175
                Layout.fillHeight: true
                Text {
                    id: typeTitle
                    text: qsTr("File Type")
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.fill: parent
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.leftMargin: 10
                    anchors.bottomMargin: 0
                }

                Text {
                    id: typeSorting
                    text: qsTr("A -> Z")
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 10
                }

                MouseArea {
                    anchors.fill: parent
                    scrollGestureEnabled: false
                    hoverEnabled: true
                    onEntered: ()=>{parent.color = "#727272";}
                    onExited: ()=>{parent.color = "#ffffff";}
                }
            }

            Rectangle {
                id: filler
                x: 0
                width: 200
                color: "#ffffff"
                Layout.minimumWidth: 0
                Layout.fillHeight: true
                Layout.fillWidth: true
            }

        }

        ListView {  // top level container
            id: listView
            implicitHeight: root.height
            implicitWidth: root.width
            anchors.top: listViewRibbon.bottom
            anchors.bottom: parent.bottom
            highlightResizeVelocity: 100
            clip: true
            synchronousDrag: true
            pixelAligned: true
            boundsMovement: Flickable.StopAtBounds
            boundsBehavior: Flickable.StopAtBounds
            anchors.topMargin: 0
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.bottomMargin: 0
            anchors.left: parent.left
            anchors.right: parent.right
            property int delegateHeight: 30

            // container for the items that go into the listview
            model: ListModel {
                id: listModel
            }

            // template for items that go into the list view
            delegate: Rectangle {
                id: listDelegate
                height: listView.delegateHeight
                width: listView.width
                color: root.color
                // container for the path object
                property var pathObject: pathObject_

                // symbol to show
                Item {
                    id: wrapper
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    width: fileTitleRect.width
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

                    Text {
                        id: text1
                        text: filename_
                        height: parent.height
                        color: "#ffffff"
                        verticalAlignment: Qt.AlignVCenter
                        leftPadding: 10
                        anchors.top: parent.top
                        anchors.left: symbol.right
                        clip: true
                    }
                }


                Text {
                    id: text2
                    text: timestamp_
                    height: parent.height
                    width: fileDateRect.width
                    color: "#ffffff"
                    verticalAlignment: Qt.AlignVCenter
                    leftPadding: 10
                    anchors.top: parent.top
                    anchors.left: wrapper.right
                }

                Text {
                    id: text3
                    text: suffix_
                    height: parent.height
                    width: fileTitleRect.width
                    color: "#ffffff"
                    verticalAlignment: Qt.AlignVCenter
                    leftPadding: 10
                    anchors.top: parent.top
                    anchors.left: text2.right
                }

                // handles hover and click events
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    property string hoverColor: "#767676"
                    // these control the hightlights
                    onEntered: (e)=> {parent.color = hoverColor;}
                    onExited: (e)=> {parent.color = root.color;}
                    // opens directorys
                    onDoubleClicked: (e)=> {list_dir(parent.pathObject);}
                }
            }

        }

    }
    // defines what to do on startup
    Component.onCompleted: list_dir(JSON.parse(fb.curdir()));

}





