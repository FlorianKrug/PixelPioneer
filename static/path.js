function getFolderPath() {
    var folderInput = document.getElementById('folderInput');
    var folderPath = folderInput.value;

    if (folderPath) {
        console.log('Selected folder path:', folderPath);
        setPath(folderPath)
    } else {
        console.log('Please enter a folder path.');
    }
}

const setPath = (folderPath) => {
    fetch('/setPath', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({path: folderPath}),
        })
}