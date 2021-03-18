import QtQuick 2.15
import QtQuick.Controls 2.15

ScrollView {
    id: terminal
    width: 600
    height: 200
    property var cmd_stack: []
    property int cmd_stack_position: 0;
    property var functionDict: ({
                                "echo": echo,
                                "help": help,
                            })

    function writeToDisplay(message, newline=true)
    {
        if (newline) {textArea.append(message);}
        else {textArea.text += message} // add the string
    }

    function startFunction()
    {
        let input = textArea.text.slice(textArea.backstop);  // take all the text
        terminal.cmd_stack.push(input);                      // add to the command stack
        terminal.cmd_stack_position = cmd_stack.length-1;    // reset the cmd stack position
        terminal.parseCommand(input);                        // parse the text for commands
    }

    function endFunction()
    {
        textArea.append("$ ");                     // set up for new line
        textArea.backstop = textArea.text.length;  // set the backstop
        textArea.cursorPositionChanged();          // emit the changed signal
        textArea.focus = true;                     // set the focus
    }

    function writeToBackend(message)
    {
        // This function is dependendent upon a
        // context object with the name "termial"
        // being exposed to qml at startup.
        terminal.write_to_backend(message)
    }

    function parseCommand(message)
    {
        message = message.trim();
        let [cmd, ...args] = message.split(' ');
        let func = terminal.functionDict[cmd];
        if (func) {func(args);}
        else
        {
            terminal.writeToDisplay(`${cmd} is not a valid command, ` +
                                    `type help for more info`);
            terminal.endFunction();
        }

    }

    function echo(args)
    {
        args = args.join(" ");
        terminal.writeToDisplay(args);
        terminal.endFunction();
    }

    function help()
    {
        let cmds = Object.keys(terminal.functionDict);
        let help_string = [`Thank you for using cnc-toolbox!\n`,
                           `the available commands are \n${cmds.join("\n")}`];
        help_string = help_string.join('');
        terminal.writeToDisplay(help_string);
        terminal.endFunction();
    }

    TextArea {
        id: textArea
        color: "green"
        height: terminal.height
        width: terminal.width
        selectByMouse: true
        background: Rectangle {
            color: "#050303"
            anchors.fill: parent
        }

        // setup the behavior where you can only go
        // back so far with your cursor.
        text: "$ ";
        font.pointSize: 12
        property int backstop: 2
        property bool wasPressed: false
        onCursorPositionChanged: {
            if (cursorPosition <= backstop){
                cursorPosition = backstop;
            }
        }

        // set up key handlers
        Keys.onPressed: {
            switch(event.key)
            {
                // limit what can be backspaced
                case Qt.Key_Backspace: {
                    if (textArea.cursorPosition <= textArea.backstop){
                        event.accepted = true;  // true prevents propagation
                    }
                    break;
                }

                // setup where hitting enter runs the command
                case Qt.Key_Return: {
                    terminal.startFunction()  // starts the function
                    event.accepted = true;    // prevents the double space
                    break;
                }

                // setup to where going up and down access cmd history
                case Qt.Key_Up: {
                    textArea.remove(textArea.backstop, textArea.length);                         // remove last command
                    textArea.insert(textArea.backstop, cmd_stack[terminal.cmd_stack_position]);  // insert prior command
                    terminal.cmd_stack_position -= terminal.cmd_stack_position ? 1 : 0;          // update the position
                    break;
                }
                case Qt.Key_Down: {
                    let increment = terminal.cmd_stack_position >= terminal.cmd_stack.length -1 ? 0 : 1;  // increment if possible
                    // if you can go forward in history
                    if (increment)
                    {
                        terminal.cmd_stack_position += increment;                                             // apply the increment
                        textArea.remove(textArea.backstop, textArea.length);                                  // remove current text
                        textArea.insert(textArea.backstop, terminal.cmd_stack[terminal.cmd_stack_position]);  // insert newer command
                    }
                    // if you are at the end of the stack
                    else {textArea.remove(textArea.backstop, textArea.length);}
                    break;
                }
                default: {
                    if (cursorPosition < textArea.backstop)
                    {
                        event.accepted = true;  // prevent typing inside of the terminal
                        cursorPosition = textArea.backstop;
                    }
                }
            }

        }
    }

}

/*##^##
Designer {
    D{i:0;height:200;width:900}
}
##^##*/
