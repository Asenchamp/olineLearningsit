let items = document.querySelectorAll('.slider .list .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');
let autoPlayInterval;
let autoPlayDelay = 5000; // Adjust the delay if necessary

// config param
let countItem = items.length;
let itemActive = 0;

// Function to stop all videos
function stopAllVideos() {
    items.forEach(item => {
        if (item.dataset.type === "video") {
            let video = item.querySelector('video');
            video.pause();
            video.currentTime = 0;
        }
    });
}

// event next click
next.onclick = function() {
    stopAllVideos();
    itemActive = itemActive + 1;
    if (itemActive >= countItem) {
        itemActive = 0;
    }
    showSlider();
}

// event prev click
prev.onclick = function() {
    stopAllVideos();
    itemActive = itemActive - 1;
    if (itemActive < 0) {
        itemActive = countItem - 1;
    }
    showSlider();
}

// auto run slider
function autoPlaySlider() {
    autoPlayInterval = setInterval(() => {
        next.click();
    }, autoPlayDelay);
}
autoPlaySlider();

function showSlider() {
    // remove item active old
    let itemActiveOld = document.querySelector('.slider .list .item.active');
    itemActiveOld.classList.remove('active');

    // active new item
    let newItem = items[itemActive];
    newItem.classList.add('active');

    // clear auto time run slider
    clearInterval(autoPlayInterval);

    if (newItem.dataset.type === "video") {
        let video = newItem.querySelector('video');
        video.play();
        video.onended = function() {
            autoPlaySlider();
        };
    } else {
        autoPlaySlider();
    }
}
