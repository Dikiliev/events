
document.getElementById("filter-button").addEventListener("click", function() {
    const categoryMenu = document.getElementById("category-menu");

    categoryMenu.classList.toggle('hidden')
});


document.getElementById("search-input").addEventListener('change', function (){

    const search_element = document.getElementById("search-input");
    console.log(search_element.value)
});
