		// set the focus to the input box
		document.getElementById("wisdom").focus();

		// Initialize the Amazon Cognito credentials provider
		AWS.config.region = 'eu-central-1'; // Region
		AWS.config.credentials = new AWS.CognitoIdentityCredentials({
		// Provide your Pool Id here
			IdentityPoolId: 'eu-central-1:2e657cfe-9b31-42e2-a4a9-4fadcb96c797',
		});

		

		var lexruntime = new AWS.LexRuntime();
		var lexUserId = 'chatbot-demo' + Date.now();
		var sessionAttributes = {};

		$(window).on('load', function() {
         firstMessage();
       })


		function pushChat() {

			// if there is text to be sent...
			var wisdomText = document.getElementById('wisdom');
			if (wisdomText && wisdomText.value && wisdomText.value.trim().length > 0) {

				// disable input to show we're sending it
				var wisdom = wisdomText.value.trim();
				wisdomText.value = '...';
				wisdomText.locked = true;

				// send it to the Lex runtime
				var params = {
					botAlias: '$LATEST',
					botName: 'LegalBot',
					inputText: wisdom,
					userId: lexUserId,
					sessionAttributes: sessionAttributes
				};
				showRequest(wisdom);
				lexruntime.postText(params, function(err, data) {
					if (err) {
						console.log(err, err.stack);
						showError('Error:  ' + err.message + ' (see console for details)')
					}
					if (data) {
						// capture the sessionAttributes for the next cycle
						sessionAttributes = data.sessionAttributes;
						// show response and/or error/dialog status
						showResponse(data);

					}
					// re-enable input
					wisdomText.value = '';
					wisdomText.locked = false;
				});
			}
			// we always cancel form submission
			return false;
		}



function setDate() {
    d = new Date()
    h = d.getHours();
    m = d.getMinutes();
   return String(h+":"+m);
    }
function msgAvatar(){
	return $('<div class="message"><figure class="avatar"><img src="img/amr.png" /></figure><span></span></div>').appendTo($('#conversation'));
}
		function showRequest(daText) {

			var conversationDiv = document.getElementById('conversation');
			var requestPara = document.createElement("P");
			requestPara.className = 'userRequest';
			requestPara.appendChild(document.createTextNode(daText));
			requestPara.appendChild(document.createElement('br'));
           requestPara.appendChild(document.createTextNode(
					setDate()
					));
			
			conversationDiv.appendChild(requestPara);
			conversationDiv.scrollTop = conversationDiv.scrollHeight;

		}

	
		function showResponse(lexResponse) {

			var conversationDiv = document.getElementById('conversation');
			var responsePara = document.createElement("P");
			responsePara.className = 'lexResponse';
			    msgAvatar();
				responsePara.appendChild(document.createTextNode(lexResponse.message));
				responsePara.appendChild(document.createElement('br'));

			     responsePara.appendChild(document.createTextNode(
					setDate()
					));
			conversationDiv.appendChild(responsePara);
			conversationDiv.scrollTop = conversationDiv.scrollHeight;
		}

		function firstMessage() {

			var conversationDiv = document.getElementById('conversation');
			var responsePara = document.createElement("P");
			responsePara.className = 'lexResponse';
			    msgAvatar();
				responsePara.appendChild(document.createTextNode("Hier ist LegalChatbot"));
				responsePara.appendChild(document.createElement('br'));
			     responsePara.appendChild(document.createTextNode(
					setDate()
					));
			conversationDiv.appendChild(responsePara);
			conversationDiv.scrollTop = conversationDiv.scrollHeight;
		}



	    function showError(daText) {

			var conversationDiv = document.getElementById('conversation');
			var errorPara = document.createElement("P");
			errorPara.className = 'lexError';
			errorPara.appendChild(document.createTextNode(daText));
			conversationDiv.appendChild(errorPara);
			conversationDiv.scrollTop = conversationDiv.scrollHeight;
		}

