function myFunction1(question_id)
    {
        console.log(roomName);

            $.ajax(
                {
                url:
                'http://127.0.0.1:8000/chat/'
                + roomName
                + '/',
                data : {
                    'flag': "satisfied",
                    'qid':question_id,
                },
                success: function (data) {
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    alert("Failure: " + errorThrown);
                }
            });

    }


    function myFunction2(question_id)
    {
        $(document).ready(function(){
            $("#chat-log").append('<li class="contact"><b>Contact Us : 7986541230<br/><a href="https://pict.edu/about-us/contact-us/">PICT Contact Us</a><b></li>');
        });

        console.log(question_id);
        var result = question_id.split(",");
        qid=result[0]
        user_asked=result[1]

            $.ajax(
                {
                url:
                'http://127.0.0.1:8000/chat/'
                + roomName
                + '/',
                data : {
                    'flag': "unsatisfied",
                    'qid':qid,
                    'userQ':user_asked
                },
                success: function (data) {
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    alert("Failure: " + errorThrown);
                }
            });

    }


        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        var flag = 0;
        var satisfiedflag = 0;
        var user = "User";

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            flag = data.flag;
            var ans=data.answer;
            console.log(ans);
            console.log(data);
            var q_asked=data.q;
            console.log(q_asked);
            var ans_id=data.ans_id;

            if(flag == 2)
            {
                ans = "What's your good name?";
                flag = 0;
            }
            else if(flag == 0)
            {
                flag = 1;
                ans = "Hello " + ans +" !!  How can i help you??"
            }

            if(ans != ' ' && ans != '\n' && ans.length != 0 )
                $('<li class="sent"><img src="{% static "assets/chatbot_icon.jpg" %}" alt="" /><p>' + ans + ' </p>\
                    <br><button name="'+ans_id+'" onclick="myFunction1(this.name)"> Satisfied</button>\
                    <button name="'+ans_id+","+q_asked+'" onclick="myFunction2(this.name)"> Unsatisfied</button></li>').appendTo($('.messages ul'));




        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        var input = document.getElementById("chat-message-input");
          input.addEventListener("keyup", function(event) {
          if (event.keyCode === 13) {
              event.preventDefault();
              document.getElementById("chat-message-submit").click();
             }
          });


       $('.submit').click(function(e){
        message = $(".message-input input").val();
        if(message != '\n' && message.length != 0)
            {
                $('<li class="replies"><img src="{% static "assets/human_icon.png" %}" alt="" /><p> '+message+' </p></li>').appendTo($('.messages ul'));
            }



            if(message.length != 0)
            {
                chatSocket.send(JSON.stringify({
                'message': message,
                'flag' : flag
                }));
            }

            $('.message-input input').val(null);
            $('.contact.active .preview').html('<span>You: </span>' + message);
            $(".messages").animate({ scrollTop: $(document).height() }, "fast");
       });


