function deleteRow(rowId1,rowId2) {
    if (confirm('Are you sure you want to delete this row?')) {
        // Send a request to the server to delete the row
        fetch('/delete_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id1: rowId1, id2: rowId2 })

        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                alert("Success! Your action has been completed.");
                document.querySelector(`#row-${rowId1}${rowId2}`).remove();
            } else {
                alert('Error deleting row');
            }
        });
    }
}

function modifyRow(rowId1, rowId2, query) {
    fetch('/modify_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ serial_number: rowId1, address: rowId2, query: query})

    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/modify_item'; 
        } else {
            alert('Error modifying row');
        }
    });

}







