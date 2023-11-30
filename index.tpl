<!DOCTYPE html>
<html lang="de">
<head>
    <title>Bildverwaltungsprogramm</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
    <h1 class="heading">Bildergalerie</h1>
    <div class="container"> <!--Container for calendar-->
            <div class="calendar">
                    <div class="date">
                        <div class="buttons">
                            <div class="year_dropdown">
                                <button class="button_year">Year</button>
                                <div class="select_year"></div>
                            </div>
                            <div class="month_dropdown">
                                <button class="button_month">Month</button>
                                <div class="select_month"></div>
                            </div>
                        </div>
                        <p class="selectedDate"></p>
                    </div>
                <div class="weekdays">
                    <div>So</div>
                    <div>Mo</div>
                    <div>Di</div>
                    <div>Mi</div>
                    <div>Do</div>
                    <div>Fr</div>
                    <div>Sa</div>
                </div>
                <div class="days">
                </div>
            </div>      
    </div>
    <div id="search_bar"><input type="text" id="tag" placeholder="Mit Tags suchen..." onkeydown="search_tags(this)"><br><br></label></div> <!--searchbar for tags-->
    <div class="exif_data_container"> <!--display EXIF-data-->
        <table class="exif_data">
            <tr><td>Datetime:</td></tr>
            <tr><td>Camera:</td></tr>
            <tr><td>Artist:</td></tr>
            <tr><td>Copyright:</td></tr>
            <tr><td>GPS Info:</td></tr>
            <tr><td>Exposure:</td></tr>
            <tr><td>Aperture:</td></tr>
            <tr><td>ISO:</td></tr>
            <tr><td>Focal length:</td></tr>
        </table>
    </div>
    <div class="navbar"> <!--Toolbar with controle buttons-->
        <div>
            <button type="button" class="buttons_nav back" title="Zurück zur Übersicht">&#8617</button>
            <p><i class="arrow left" title="Bild zurück"></i></p>
            <p><i class="arrow right" title="Bild weiter"></i></p>
        </div>
        <div>
            <div class="text">Diashow Timer in s:</div>
            <input type="text" class="diashow_timer" style="width: 22px; height: 22px; margin: 5px;" title="Diashow Timer">
            <i class="gg-play-button-r diashow" title="Diashow starten"></i>
            <i class="fa fa-trash-o bin" style="font-size: 24px; height: 28px; margin: 3px;" title="Doppelklick zum Bild löschen"></i>
        </div>
    </div>
    <div class="pictures"> <!--container for displaying image relevant stuff-->
        <div class="images_gallery"></div>
        <div class="content"></div>
        <div class="date_list"></div>
        <div class="tags_show">
            <input class="add_tags" type="text" id="tag" placeholder="Tags" onkeydown="add_tags(this)">
        </div>
    </div>
    <script src="script.js"></script> <!--include JavaScript -->
</body>
</html>