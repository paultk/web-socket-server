/*class Board {
 constructor(context) {
 this.context=context;
 this.mouse_down=0;

 this.ws = new WebSocket("ws://localhost:3001");

 this.ws.onerror = (error) => {
 $("#connection_label").html("Not connected");
 };

 this.ws.onopen = () => {
 $("#connection_label").html("Connected");
 };

 this.ws.onmessage = (event) => {
 var json=JSON.parse(event.data);
 //      console.log(json)
 if(json.line) {
 this.draw_line(json.line.x1, json.line.y1, json.line.x2, json.line.y2);
 }
 };

 this.ws.onclose = function(message) {
 $("#connection_label").html("Not connected");
 };
 }

 draw_line(x1, y1, x2, y2) {
 this.context.lineWidth=1;
 this.context.beginPath();
 this.context.moveTo(x1, y1);
 this.context.lineTo(x2,y2);
 this.context.closePath();
 this.context.stroke();
 };

 on_mouse_down(event) {
 this.mouse_down=1;
 this.last_x=event.offsetX;
 this.last_y=event.offsetY;
 }

 on_mouse_up(event) {
 this.mouse_down=0;
 };

 on_mouse_move(event) {
 if(this.mouse_down>0) {
 var x=event.offsetX;
 var y=event.offsetY;

 if(this.ws.readyState==1) {
 var json={"line": { "x1": this.last_x, "y1": this.last_y, "x2": x, "y2": y}};

 this.ws.send(JSON.stringify(json));
 }

 this.last_x=x;
 this.last_y=y;
 }
 }
 }

 var board;
 //When this file is fully loaded, initialize board with context*/

class MessageBoard {

    constructor(context) {
        this.context=context;
        this.mouse_down=0;

        this.ws = new WebSocket("ws://localhost:3001/");

        this.ws.onerror = (error) => {
            $("#connection_label").html("Not connected");
        };

        this.ws.onopen = () => {
            $("#connection_label").html("Connected");
        };

        this.ws.onmessage = (event) => {
            console.log(event)
            var json=JSON.parse(event.data);
            console.log('json');
            console.log(json['message']);
            let message = json['message'];
            let time = new Date();

            $('#ul').append(
                '<li><span style="color: ' + message.color + '">' + message.name + ' wrote: ' + message.messageText + " at" +
                time.getHours() + ':' + time.getMinutes() + '</span></li>'
            )

        };

        this.ws.onclose = function(message) {
            $("#connection_label").html("Not connected");
        };

    }

    sendMessage(message) {
        this.ws.send(message);
    };
}
var messageBoard;
$(document).ready(function(){
    messageBoard = new MessageBoard(null);
    var name;
    var color;


    $('#button1').click( () => {
        console.log('dd')
});
    $('#sendMessageButton').click( () => {
        message = $('#inputField').val();

    console.log(message);
    // var json={"message": { "name": name, "messageText": message, 'time': new Date(), 'color': color}};
    // messageBoard.sendMessage(JSON.stringify(json));
    messageBoard.sendMessage(message)

});

    $('#saveName').click( () => {
        $('#nameDiv').hide();
    $('#afterNameRegistration').css('visibility', 'visible');
    color = $('#color').val();
    name =$('#name').val();
})

    /*
     () => {
     console.log('yea');
     });
     */
    /*
     board = new Board($('#board')[0].getContext('2d'));

     $('body').mousedown((event) => {
     board.on_mouse_down(event);
     }).mouseup((event) => {
     board.on_mouse_up(event);
     });

     $('#board').mousemove((event) => {
     board.on_mouse_move(event)
     });*/
});