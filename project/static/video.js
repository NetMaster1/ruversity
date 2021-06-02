//VIDEOJS PLAYER SETTINGS
let player = videojs('video', {

    width: 1080,
    controls: true,
    currentTimeDisplay: true,
    playbackRates: [0.5, 0.75, 1, 1.25, 1.5],
    // fluid: true,
    userActions: {
        hotkeys: true
    }  
}
)

// player.aspectRatio('16:9');//default mode
// player.width(720);
// player.height(405);


player.on('ended', checked);

function checked() {
    alert('You finished the lecture');
  
   
}





// player.zoomrotate({
//     rotate: 180,
//     zoom: 1.5
// });

// console.log(player);
// console.log('Once Again testing....Ok')