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
                console.log(`#row-${rowId1}${rowId2}`);
                document.querySelector(`#row-${rowId1}${rowId2}`).remove();
            } else {
                alert('Error deleting row');
            }
        });
    }
}
// rowId1, rowId2 分別為 serial_number, 土地位置建物門牌
function modifyRow(rowId1,rowId2) {

}

