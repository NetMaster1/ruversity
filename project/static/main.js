//get all the stars
const one = document.getElementById('first')
const two = document.getElementById('second')
const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')

const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const handleStarSelect = (size) => {
    const children = form.children
    for (let i = 0; i < children.length; i++) {
        if (i <= size) {
            children[i].classList.add('checked')
        }
        else {
            children[i].classList.remove('checked')
        }
    }
}

//longer version to be optimized
const handleSelect = (selection) => {
    switch (selection) {
        case 'first': {
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(1)
            return
        }
        case 'second': {
            // one.classList.add('checked')
            // two.classList.add('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(2)
            return
        }
        case 'third': {
            // one.classList.add('checked')
            // two.classList.add('checked')
            // three.classList.add('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(3)
            return
        }
        case 'fourth': {
            // one.classList.add('checked')
            // two.classList.add('checked')
            // three.classList.add('checked')
            // four.classList.add('checked')
            // five.classList.remove('checked')
            handleStarSelect(4)
            return
        }
        case 'fifth': {
            // one.classList.add('checked')
            // two.classList.add('checked')
            // three.classList.add('checked')
            // four.classList.add('checked')
            // five.classList.add('checked')
            handleStarSelect(5)
            return
        }
    }
}

if (one) {
    const arr = [one, two, three, four, five]
    arr.forEach(item => item.addEventListener('mouseover', (event) => { handleSelect(event.target.id) }))
    arr.forEach(item => item.addEventListener('click', (event) => {
        const val = event.target.id

        form.addEventListener('submit', e => {
            e.preventDefault()
            const id = e.target.id
        })
    }))

}

//================================
//let starsTotal = 5;
//let rating = 4;
//let subjects = '{{ subjects }}';
//run getRatings when DOM loads
//document.addEventListener('DOMContentLoaded', getRatings)

//function getRatings() {
//for (let subject in subjects) {
//get percentage value
//const starPercentage=(ratings[rating]/starTotal)*100;
//round to nearest 10
//const starPercentageRounded='${Math.round(starPercentage / 10)*10}%';
//set width of star-inner to percentage
//document.querySelector('.${rating} .stars-inner').style.width=starPercentageRounded;}
//let starPercentage = (rating / starsTotal) * 100;
// console.log(starPercentage)
//const starPercentageRounded = '${Math.round(starPercentage / 10) * 10 } %';
//console.log(starPercentageRounded)
//const starPercentageRounded = '${Math.round(starPercentage / 10) * 10 } %';
//console.log(starPercentageRounded);
//let colorVar = 'blue'
//document.querySelector('.sample').style.color = colorVar;
// let value = '80%';
//var width = document.querySelector(' .stars-inner').style.width = value;
// console.log(width)
//document.querySelector('.sample').style.color = red;
//}
//}

//VIDEOJS PLAYER SETTINGS
console.log('Testing....Ok')

let player = videojs('my-video', {
    
    controls: true,
    playbackRates: [0.5, 0.75, 1, 1.25, 1.5],
    fluid: true,
    poster: 'https://picsum.photos/800/450',
    userActions: {
        hotkeys: true
    }  
})

// let quality = player.qualityLevels();
    
player.on('ended', function () {
    alert('You finished the lecture')
});







