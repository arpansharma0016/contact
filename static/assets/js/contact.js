document.getElementById('save_contact').addEventListener('click', function() {
    var name = document.getElementById('name').value
    var email = document.getElementById('email').value
    var data = { name: name, email: email }
    var url = "/save_contact/"
    $.ajax({
        'type': 'POST',
        'url': url,
        'data': JSON.stringify(data),
        'success': function(response) {
            if (response.status == "success") {
                var data = document.getElementById('table').innerHTML
                document.getElementById('table').innerHTML = `
                <tr id="tr-${response.id}">
                    <td>${response.name}</td>
                    <td>${response.email}</td>
                    <td>
                        <button type="button" class="btn btn-warning" onclick="edit_contact(event, ${response.id})">Edit</button>
                    </td>
                    <td>
                        <button type="button" class="btn btn-danger" onclick="delete_contact(event, ${response.id})">Delete</button>
                    </td>
                </tr>
                ` + data
                document.getElementById('email').value = ''
                document.getElementById('name').value = ''
                document.getElementById('succ').innerText = 'Contact Saved!'
                setTimeout(() => {
                    document.getElementById('succ').innerText = ''
                }, 1000)

            } else {
                document.getElementById('error').innerText = response.message
                setTimeout(() => {
                    document.getElementById('error').innerText = ''
                }, 1000)
            }
        },
        'error': function(error) {
            alert(error)
        },
        'dataType': 'json',
        'contentType': 'application/json; charset=UTF-8',
    })
})

function delete_contact(e, id) {
    e.preventDefault()
    var id = parseInt(id)
    var url = `/delete_contact-${id}/`
    $.get(url, function(response) {
        if (response.status == 'success') {
            document.getElementById('tr-' + id).remove()
            document.getElementById('succ').innerText = 'Deleted Sucessfully!'
            setTimeout(() => {
                document.getElementById('succ').innerText = ''
            }, 1000)
        }
    })
}

function edit_contact(e, id) {
    e.preventDefault()
    var id = parseInt(id)
    var url = `/edit_contact-${id}/`
    $.get(url, function(response) {
        if (response.status == 'success') {
            document.getElementById('editname').value = response.name
            document.getElementById('editemail').value = response.email
            document.getElementById('hiddenid').value = id
        }
        $('#exampleModal').modal('toggle')
    })
}

document.getElementById('editbutton').addEventListener('click', function(e) {
    e.preventDefault()
    var id = document.getElementById('hiddenid').value
    var url = `/edit-${id}/`
    var name = document.getElementById('editname').value
    var email = document.getElementById('editemail').value
    var data = { name: name, email: email }
    $.ajax({
        'type': 'POST',
        'url': url,
        'data': JSON.stringify(data),
        'success': function(response) {
            if (response.status == 'success') {
                document.getElementById('tr-' + response.id).innerHTML = `
                <td>${response.name}</td>
                <td>${response.email}</td>
                <td>
                    <button type="button" class="btn btn-warning" onclick="edit_contact(event, ${response.id})">Edit</button>
                </td>
                <td>
                    <button type="button" class="btn btn-danger" onclick="delete_contact(event, ${response.id})">Delete</button>
                </td>
                `
                document.getElementById('succ').innerText = 'Edited Sucessfully!'
                setTimeout(() => {
                    document.getElementById('succ').innerText = ''
                }, 1000)

                $('#exampleModal').modal('toggle')

                document.getElementById('editname').value = ''
                document.getElementById('editemail').value = ''

            } else {
                document.getElementById('editerror').innerText = response.message
                setTimeout(() => {
                    document.getElementById('editerror').innerText = ''
                }, 1000)
            }
        },
        'error': function(error) {
            alert(error)
        },
        'dataType': 'json',
        'contentType': 'application/json; charset=UTF-8',
    })
})