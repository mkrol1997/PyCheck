function checkRoom() {
    var room_id = document.getElementById('room-id').value;

    fetch('/find_channel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "channel": room_id,
        }),
    })
    .then(response => response.json())
    .then(data => {
    console.log(data);
        if (data.status === 200) {
            window.location.href = data.redirect_url;
        } else {
            document.getElementById('search_warning').innerText = 'Room with given code does not exist.. Try again!'
        }
    })
    .catch(error => {
        console.error(error);
    });
}
