function update_state(resource, val) {
        let data = {"resource": resource, "val": val};

        fetch("/update", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(function (data) {
                document.getElementById("momentum").innerHTML = data.momentum;
                document.getElementById("threat").innerHTML = data.threat;
            })
}

