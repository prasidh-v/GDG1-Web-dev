

const btnAdd = document.getElementById('btn-add');
const addClothesModal = document.getElementById('addClothesModal');
const closeModal = document.getElementById('closeModal');
const saveClothing = document.getElementById('saveClothing');
const searchInput = document.getElementById('searchInput');


let clothingItems = [];


btnAdd.addEventListener('click', () => {
    addClothesModal.style.display = 'block';
});

closeModal.addEventListener('click', () => {
    addClothesModal.style.display = 'none';
});

saveClothing.addEventListener('click', () => {
    const clothingTitle = document.getElementById('clothingTitle').value;
    const clothingType = document.getElementById('clothingType').value;
    const clothingImage = document.getElementById('clothingImage').files[0];

    if (clothingTitle && clothingType && clothingImage) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const clothingData = {
                title: clothingTitle,
                type: clothingType,
                image: e.target.result,
            };

            clothingItems.push(clothingData);
            displayClothingItems();
            addClothesModal.style.display = 'none';
        };

        reader.readAsDataURL(clothingImage);
    } else {
        alert('Please fill in all fields.');
    }
});


function displayClothingItems() {
    const sections = {
        'top-wear': document.getElementById('top-wear'),
        'bottom-wear': document.getElementById('bottom-wear'),
        footwear: document.getElementById('footwear'),
        accessories: document.getElementById('accessories'),
    };


    for (let section in sections) {
        sections[section].innerHTML = '';
    }

    clothingItems.forEach(item => {
        const clothingItem = document.createElement('div');
        clothingItem.classList.add('clothing-item');
        clothingItem.innerHTML = `<img src="${item.image}" alt="${item.title}">`;

        sections[item.type].appendChild(clothingItem);
    });
}


searchInput.addEventListener('input', function () {
    const query = searchInput.value.toLowerCase();
    clothingItems.forEach(item => {
        const clothingItems = document.querySelectorAll('.clothing-item');
        clothingItems.forEach(cloth => {
            const imgAlt = cloth.querySelector('img').alt.toLowerCase();
            if (!imgAlt.includes(query)) {
                cloth.style.display = 'none';
            } else {
                cloth.style.display = 'block';
            }
        });
    });
});