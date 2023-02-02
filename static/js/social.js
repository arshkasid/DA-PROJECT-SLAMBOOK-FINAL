// js function to show notifications from navbar
// it uses the class of container and opens or closes it depending upon its state
function showNotifications() {
	const container = document.getElementById('notification-container');

	if (container.classList.contains('d-none')) {
		container.classList.remove('d-none');
	} else {
		container.classList.add('d-none');
	}
}
// getcookie funtion taken from django library to get cookies in order to show messages at various prompts like notifs or searching user from search
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// js funtion to remove funtion from the notification toggle
function removeNotification(removeNotificationURL, redirectURL) {
	const csrftoken = getCookie('csrftoken');
	let xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {
			if (xmlhttp.status == 200) {
				window.location.replace(redirectURL);
			} else {
				alert('There was an error');
			}
		}
	};

	xmlhttp.open("DELETE", removeNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xmlhttp.send();
}

// js function to share
function shareToggle(parent_id) {
	const row = document.getElementById(parent_id);

	if (row.classList.contains('d-none')) {
		row.classList.remove('d-none');
	} else {
		row.classList.add('d-none');
	}
}

// it takes tags, split them into words and returns tags as words
// we take elements, loop through them, get text of the body, split text, check if first character is #, 
function formatTags() {
	const elements = document.getElementsByClassName('body');
	for (let i = 0; i < elements.length; i++) {
		let bodyText = elements[i].children[0].innerText;

		let words = bodyText.split(' ');

		for (let j = 0; j < words.length; j++) {
			if (words[j][0] === '#') {
				//creating a link that goes to the page
				let replacedText = bodyText.replace(/\s\#(.*?)(\s|$)/g, ` <a href="/social/explore?query=${words[j].substring(1)}">${words[j]}</a>`);
				elements[i].innerHTML = replacedText;
			}
		}
	}
}

formatTags();