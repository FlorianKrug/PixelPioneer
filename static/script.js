const datepickerInput = document.querySelector('.selectedDate');
const datepickerCalendar = document.querySelector('.calendar');
const date = new Date();
var current_year = date.getFullYear();
var current_month = date.getMonth() + 1;
const date_year = date.getFullYear();
datepickerInput.textContent = date.getDate()+ "-"+ current_month + "-"+ date.getFullYear() ;

let picture_days = [];
let picture_years = [];
let picture_months = [];

var current_picture;

const months = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "Semptember",
    "Oktober",
    "November",
    "Dezember",
];

//http requests for years, months and days
const getPicturesDay = () => {
    current_month = date.getMonth() + 1;
    current_year = date.getFullYear();
    fetch('/api/getPicturesDay', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({year: current_year, month: `${current_month < 10 ? '0' : ''}${current_month}`, day: []}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(updatedData => {
            picture_days = updatedData['days'];
            renderCalendar();
        })
        .catch(error => {
            console.error('Error updating data:', error);
        });
}

const getPicturesYear = () => {
    fetch('/api/getPictureYears', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({year: []}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(updatedData => {
            picture_years = updatedData['years'];
        })
        .catch(error => {
            console.error('Error updating data:', error);
        });
}

const getPicturesMonth = () => {
    current_year = date.getFullYear();
    fetch('/api/getPicturesMonths', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({year: current_year}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(updatedData => {
            picture_months = updatedData['months']
        })
        .catch(error => {
            console.error('Error updating data:', error);
        });
}

//http request for exif-data
const getEXIF = () => {
    fetch('/api/getEXIF', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({exif: current_picture}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(updatedData => {
            const container = document.querySelector(".exif_data");
            let input = "";
            input += `<tr><td>Aufnahmedatum: </td><td>${updatedData['datetime']}</td></tr>`;
            input += `<tr><td>Kamera: </td><td>${updatedData['camera']}</td></tr>`;
            input += `<tr><td>Artist:</td><td>${updatedData['artist']}</td></tr>`;
            input += `<tr><td>Copyright:</td><td>${updatedData['copyright']}</td></tr>`;
            input += `<tr><td>GPS Info:</td><td>${updatedData['gps']}</td></tr>`;
            input += `<tr><td>Belichtungszeit:</td><td>${updatedData['exposoure']} sec</td></tr>`;
            input += `<tr><td>Blende:</td><td>${updatedData['fnum']}</td></tr>`;
            input += `<tr><td>ISO:</td><td>${updatedData['iso']}</td></tr>`;
            input += `<tr><td>Brennweite:</td><td>${updatedData['focal_length']} mm</td></tr>`;
            container.innerHTML = input;
        })
        .catch(error => {
            console.error('Error updating data:', error);
        });
}

//Calendar
const renderCalendar = () => {
    date.setDate(1);

    const monthDays = document.querySelector('.days');
    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const firstDayIndex = date.getDay();
    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();
    const nextDays = 7 - lastDayIndex - 1;
    const years_menu = document.querySelector('.select_year');
    const months_menu = document.querySelector('.select_month')

    current_month = date.getMonth() + 1;

    let days = "";
    let sel_years = "";
    let sel_months = "";

    //create previous days
    for (let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
    }

    //create days per month
    for (let i = 1; i <= lastDay; i++) {
        if(i < 10){
            i = `0${i}`
        }
        if(picture_days.includes(i.toString())){
            days += `<div class="picture_available">${i}</div>`;
        }
        else{
            days += `<div class="not_available">${i}</div>`;
        }
    }

    //create next days
    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date">${j}</div>`;
    }

    //create list with years, starting from oldes picture
    for (let i = date_year; i >= Math.min(...picture_years); i--){
        if(picture_years.includes(i.toString())){
            sel_years += `<a class="year picture_available" href="#" onclick="getYear(this)">${i}</a>`;
        }
        else{
            sel_years += `<a class="year not_available" href="#" onclick="getYear(this)">${i}</a>`;
        }
    }

    //create list with months
    for (i = 1; i<= 12; i++){
        x = i - 1;
        if(i < 9){
            i = `0${i}`;
        }
        if(picture_months.includes(i.toString())){
            sel_months += `<a class="month picture_available" href="#" onclick="getMonth(this)">${x < 9 ? '0' : ''}${x+1} - ${months[x]}</a>`;
        }
        else{
            sel_months += `<a class="month not_available" href="#" onclick="getMonth(this)">${x < 9 ? '0' : ''}${x+1} - ${months[x]}</a>`;
        }
    }

    datepickerInput.textContent = date.getDate()+ "-"+ current_month + "-"+ date.getFullYear() ;
    monthDays.innerHTML = days;
    years_menu.innerHTML = sel_years;
    months_menu.innerHTML = sel_months;
}

//display image
function show_image(element) {
    var innerImage = element.querySelector('img');
    if(innerImage) {
        document.querySelector('.images_gallery').classList.add('images_gallery_hide')
        document.querySelector('.images_gallery').classList.remove('images_gallery')
        current_picture = innerImage.getAttribute('src');
        if(document.querySelector('.content_hide')){
            document.querySelector('.content_hide').classList.add('content')
            document.querySelector('.content').classList.remove('content_hide')
        }
        document.querySelector('.content').innerHTML = `<img class="image_content" src="${current_picture}"></img>`;
        //get and display exif-data
        getEXIF();
        //read and display tags
        readTags();
    }
}

const clear_exif = () => {
    document.querySelector('.exif_data').innerHTML = '<tr><td>Aufnahmedatum:</td></tr>'+
     '<tr><td>Kamera:</td></tr>'+ 
     '<tr><td>Artist:</td></tr>'+ 
     '<tr><td>Copyright:</td></tr>'+ 
     '<tr><td>GPS Info:</td></tr>'+ 
     '<tr><td>Belichtungszeit:</td></tr>'+ 
     '<tr><td>Blende:</td></tr>'+ 
     '<tr><td>ISO:</td></tr>'+ 
     '<tr><td>Brennweite:</td></tr>'
}

//buttons in Toolbar
document.querySelector('.back').addEventListener('click', event=> {
    document.querySelector('.images_gallery_hide').classList.add('images_gallery');
    document.querySelector('.images_gallery_hide').classList.remove('images_gallery_hide');
    document.querySelector('.content').innerHTML = "";
    clear_exif()
    document.querySelector('.add_tags').value = ''
})

document.querySelector('.left').addEventListener('click', event => {
    const images = document.querySelectorAll('.thumbnail');
    for(var i = 0; i < images.length; i++){
        if(images[i].getAttribute('src').toString() == current_picture){
            current_picture = images[i-1].getAttribute('src').toString();
            document.querySelector('.content').innerHTML = `<img class="image_content" src="${current_picture}"></img>`;
            getEXIF();
            readTags();
        }
    }
})

document.querySelector('.right').addEventListener('click', event => {
    const images = document.querySelectorAll('.thumbnail');
    for(var i = 0; i < images.length; i++){
        if(images[i].getAttribute('src').toString() == current_picture){
            current_picture = images[i+1].getAttribute('src').toString();
            document.querySelector('.content').innerHTML = `<img class="image_content" src="${current_picture}"></img>`;
            getEXIF();
            readTags();
            break;
        }
    }
})

document.querySelector('.diashow').addEventListener('click', event => {
    diashow()
})

document.querySelector('.bin').addEventListener('dbclick', event => {
    fetch('api/bin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({src: current_picture}),
    })

})

//controle diashow
function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}
  
async function diashow() {
    try{
        document.querySelector('.images_gallery').classList.add('images_gallery_hide')
        document.querySelector('.images_gallery').classList.remove('images_gallery')
        document.querySelector('.content_hide').classList.add('content')
        document.querySelector('.content').classList.remove('content_hide')
    }
    catch(error){
        console.error(error)
    }
    const images = document.querySelectorAll('.thumbnail');
    if (document.querySelector('.diashow_timer').value == ""){ //set diashow timer to 4 seconds when no time is given
        document.querySelector('.diashow_timer').value = 4
    }
    for(var i = 0; i < images.length; i++){
        current_picture = images[i].getAttribute('src').toString();
        document.querySelector('.content').innerHTML = `<img class="image_content" src="${current_picture}"></img>`;
        getEXIF();
        await sleep(parseInt(document.querySelector('.diashow_timer').value + "000"))
    }
}

//read tags

const readTags = () => {
    fetch('/api/tags_read', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({src: current_picture}),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
                }
                return response.json();
            })
            .then(updatedData => {
                document.querySelector('.add_tags').value = updatedData['keywords'].join(', ')
            })
            .catch(error => {
                console.error('Error updating data:', error);
            });
}

// write tags

function add_tags(element) {
    if(event.key === 'Enter') {
        fetch('/api/tags_write', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({src: current_picture, keywords:element.value}),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                    }
                    return response.json();
                })
                .then(updatedData => {
                    readTags()
                })
                .catch(error => {
                    console.error('Error updating data:', error);
                });      
    }
}

//search with tags and create list

function search_tags(element){
    if(event.key === 'Enter') {
        fetch('/api/tags_search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({keywords:element.value.split(', ')}),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                    }
                    return response.json();
                })
                .then(updatedData => {
                    if(document.querySelector('.date_list_hide')){
                        document.querySelector('.date_list_hide').classList.add('date_list')
                        document.querySelector('.date_list').classList.remove('date_list_hide')
                    }
                    clear_exif()
                    document.querySelector('.add_tags').value = ''
                    try{
                        if(document.querySelector('.content').getElementsByTagName('img').length > 0){
                            document.querySelector('.content').classList.add('content_hide')
                            document.querySelector('.content_hide').classList.remove('content')
                        }
                    }
                    catch{
                    }
                    if(document.querySelector('.images_gallery')){
                        document.querySelector('.images_gallery').classList.add('images_gallery_hide')
                        document.querySelector('.images_gallery_hide').classList.remove('images_gallery')
                    }
                    console.log(updatedData)
                    let list = ""
                    for(let i = 0; i  < updatedData['dates'].length; i++){
                        list += `<button class="date_list_button" title="Tags des ersten Bildes" onclick="getDateFromButton(this)">${updatedData['dates'][i]}   (${updatedData['keywords'][i]})</button>`
                    }
                    document.querySelector('.date_list').innerHTML = list
                })
                .catch(error => {
                    console.error('Error updating data:', error);
                });  
    }
}

//buttons in tag list
function getDateFromButton(element){
    document.querySelector('.add_tags').value = ''
    string_date = element.textContent.split(" ")[0];
    string_date = string_date.split(".");
    console.log(string_date);
    date.setFullYear(string_date[0]);
    date.setMonth(string_date[1] - 1);
    document.querySelector('.date_list').classList.add('date_list_hide')
    document.querySelector('.date_list_hide').classList.remove('date_liste')
    getImages(string_date[0], string_date[1], string_date[2]);
    document.querySelector('.button_month').innerHTML = `${string_date[1]} - ${months[parseInt(string_date[1]) - 1]}`
    document.querySelector('.button_year').innerHTML = string_date[0]
    getPicturesDay()
    setTimeout(function() {datepickerInput.textContent = `${string_date[2]}-${string_date[1]}-${string_date[0]}`}, 100)
}

//buttons in Calendar
function getYear(element){
    if(element.classList.contains('year')){
        date.setFullYear(element.textContent);
        getPicturesMonth();
        getPicturesDay();
        document.querySelector('.button_year').innerHTML = element.textContent;
    }
}

function getMonth(value){
    if(value.classList.contains('month')){
        date.setMonth(value.textContent.split(" ")[0] - 1)
        getPicturesDay();
        document.querySelector('.button_month').innerHTML = value.textContent;
    }
}

const getImages = (selectedYear, selectedMonth, selectedDay) => {
    fetch('http://127.0.0.1:8080/api/sendData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({year: selectedYear, month: `${selectedMonth}`, day: `${selectedDay}`}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(updatedData => {
            if(document.querySelector('.images_gallery_hide')){
                document.querySelector('.images_gallery_hide').classList.add('images_gallery')
                document.querySelector('.images_gallery').classList.remove('images_gallery_hide')
            }
            document.querySelector('.add_tags').value = ''
            const gallery = document.querySelector('.images_gallery')
            let images = ""
            const imageList = updatedData['bilder']
            for(let i = 0; i < imageList.length; i++){
                images += `<div class="images_gallery_item" onclick="show_image(this)">
                <img class="thumbnail" src="${imageList[i].replace('static/', '')}" alt="${imageList[i].replace('static/', '')}">
                </div>`
            };
            gallery.innerHTML = images;
        })
        .catch(error => {
            console.error('Error updating data:', error);
    });
}

//display images for selected day
document.querySelector('.days').addEventListener('click', (event) => {
    try{
        if(document.querySelector('.content').getElementsByTagName('img').length > 0){
            document.querySelector('.content').classList.add('content_hide')
            document.querySelector('.content_hide').classList.remove('content')
        }
    }
    catch{
    }
    try{
        if(document.querySelector('.date_list').getElementsByTagName('button').length > 0){
            document.querySelector('.date_list').classList.add('date_list_hide')
            document.querySelector('.date_list_hide').classList.remove('date_list')
        }
    }
    catch{
    }
    if(document.querySelector('.images_gallery_hide')){
        document.querySelector('.images_gallery_hide').classList.add('images_gallery')
        document.querySelector('.images_gallery').classList.remove('images_gallery_hide')
    }
    clear_exif()
    const selectedDay = event.target.textContent;
    var selectedMonth = date.getMonth() + 1; 
    current_month = selectedMonth;
    const selectedYear = date.getFullYear();
    if(selectedMonth < 10){
        selectedMonth = "0" + selectedMonth
    }
    const formattedDate = `${selectedDay}-${selectedMonth}-${selectedYear}`;
    datepickerInput.textContent = formattedDate;
    getImages(selectedYear, selectedMonth, selectedDay)
});



//build calendar
getPicturesYear();
getPicturesMonth();
getPicturesDay();