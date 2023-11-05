let events;
let categories;

function initialize(events, categories){
    console.log('initialize')

    this.events = events
    this.categories = categories
}


console.log('load')

document.getElementById("filter-button").addEventListener("click", function() {
    const categoryMenu = document.getElementById("category-menu");

    categoryMenu.classList.toggle('hidden')
});


document.getElementById("search-input").addEventListener('change', function (){

    const search_element = document.getElementById("search-input");
    console.log(search_element.value)
});

document.getElementById('start-new-button').addEventListener('click', function (){
    const btn = document.getElementById('start-new-button');

    if (!btn.classList.contains('active')){
        btn.classList.add('active');
        document.getElementById('start-near-button').classList.remove('active');
    }
});

document.getElementById('start-near-button').addEventListener('click', function (){
    const btn = document.getElementById('start-near-button');

    if (!btn.classList.contains('active')){
        btn.classList.add('active');
        document.getElementById('start-new-button').classList.remove('active');
    }
});