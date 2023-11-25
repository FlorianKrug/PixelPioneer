<!DOCTYPE html>
<html lang="de">
<head>
    <title>Bildverwaltungsprogramm</title>
    <!-- <link rel="stylesheet" href="style.css"> -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
    <h1>Path to pictures</h1>
    <label for="folderInput">Select Folder:</label>
    <input type="text" id="folderInput" value="{{dirPath}}" style="width: 300px;">
    <button onclick="getFolderPath()">Set Folder Path</button>
    <script src="path.js"></script>
</body>
</html>