// =======================================================================
// Открытие и закрытие меню
// =======================================================================
let nav = document.querySelector('.nav');
let menuOpenBtn = document.querySelector('.nav__bars-open');
let menuExitBtn = document.querySelector('.nav__bars-exit');

let menuOpenListener;

menuExitBtn.addEventListener('click', function (e) {
    e.preventDefault();
    nav.style.left = '-110%';

});

menuOpenBtn.addEventListener('click', function (e) {
    e.preventDefault();
    nav.style.left = '0';
});

// =======================================================================
// Перенос формы поиска
// =======================================================================
let header = document.querySelector('.header');
let headerList = document.querySelector('.header__list');
let headerListCategories = document.querySelector('.header__list._categories');

let searchForm = document.querySelector('.header__search');
let widthForJump = 740;

formControll(widthForJump);
window.addEventListener('resize', (e) => formControll(widthForJump));

function formControll(minwidth) {
    if (minwidth <= window.innerWidth) {
        headerList.before(searchForm);
    } else {
        headerListCategories.before(searchForm);
    }
}

if (window.innerWidth < 440) document.querySelector('.header__list-links._offise').style = "display:none";


window.addEventListener('resize', (e) => {
    if (window.innerWidth < 440) {
        document.querySelector('.header__list-links._offise').style = "display:none";
    }
    else {
        document.querySelector('.header__list-links._offise').style = "display:flex";
    }
});


// =======================================================================
// Работа со слайдером текущего продутка
// =======================================================================
try {

    let productSliderItems = [...document.querySelectorAll('.product__slider-item')];
    let indicators = document.querySelectorAll('.indicators__links');

    indicators.forEach((item, i) => {
        item.addEventListener('click', function (e) {
            productSliderItems.forEach((el, index) => {
                el.classList.remove('active');
                indicators[index].classList.remove('active');
            });
            productSliderItems[i].classList.add('active');
            indicators[i].classList.add('active');
        });
    });


    let btnPrev = document.querySelector('.product__slider-btns .btn__prev');
    let btnNext = document.querySelector('.product__slider-btns .btn__next');

    let curentIndex = 0;

    btnPrev.addEventListener('click', (e) => {

        productSliderItems.forEach((item, i) => {
            if (item.classList.contains('active')) curentIndex = i;
            item.classList.remove('active');
            indicators[i].classList.remove("active");

        });

        if (curentIndex == productSliderItems.length - 1) productSliderItems[0].classList.add("active");
        else productSliderItems[curentIndex + 1].classList.add("active");

        if (curentIndex == productSliderItems.length - 1) {
            productSliderItems[0].classList.add("active");
            indicators[0].classList.add("active");
        }
        else {
            productSliderItems[curentIndex + 1].classList.add("active");
            indicators[curentIndex + 1].classList.add("active");
        }


    });
    btnNext.addEventListener('click', (e) => {

        productSliderItems.forEach((item, i) => {
            if (item.classList.contains('active')) curentIndex = i;
            item.classList.remove('active');
            indicators[i].classList.remove("active");
        });

        if (curentIndex == 0) {
            productSliderItems[productSliderItems.length - 1].classList.add("active");
            indicators[productSliderItems.length - 1].classList.add("active");
        }
        else {
            productSliderItems[curentIndex - 1].classList.add("active");
            indicators[curentIndex - 1].classList.add("active");
        }
    });
} catch (error) { }



// =======================================================================
// Корзина. Переброс иформации из одной части элемента в другую 
// =======================================================================
try {
    let basketItems = document.querySelectorAll('.basket__item');

    basketItems.forEach(el => {

        let basketDelete = el.querySelector('.basket__delete');
        let basketText = el.querySelector('.basket__item-text');;
        let basketOptions = el.querySelector('.basket__options');

        function basketContloll() {
            if (window.innerWidth <= 504) {
                basketDelete.after(basketOptions);
            } else {
                basketText.after(basketOptions);
            }
        }

        basketContloll();

        window.addEventListener('resize', basketContloll);
    });
} catch (error) { }


// =======================================================================
// Таблица. Полный копирайт информации из одной части объекта в другую 
// =======================================================================
try {
    let tabelInfo = [...document.querySelectorAll('.profile__tabel-data')];

    let tabelTitle = document.querySelectorAll('.profile__title-adaptive');

    let _arr = [];
    let tabelInfoParse = [];

    tabelInfo.forEach((item, i) => {
        if (i % 3 == 0 && i != 0) {
            tabelInfoParse.push(_arr);
            _arr = [];
        }
        _arr.push(item);

        if (i === tabelInfo.length - 1) tabelInfoParse.push(_arr);
    });


    tabelTitle.forEach((item, i) => {
        let newElement = document.createElement('div');
        newElement.className = 'profile__tabel-adaptive';
        newElement.innerHTML = `        
            <p>Цена:<span>${tabelInfoParse[i][0].innerHTML}</span></p>
            <p>Дата:<span>${tabelInfoParse[i][1].innerHTML}</span></p>
            <p>Статус:<span>${tabelInfoParse[i][2].innerHTML}</span></p>
        `;
        item.append(newElement);
    });


} catch (error) { }


// =======================================================================
// Добавление в избранное(Только анимация сердца)
// =======================================================================
try {
    let heart = [...document.querySelectorAll('.products__item-heart')];

    heart.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            item.classList.toggle('active');
        });
    });

} catch (error) { }


// Raiting
// ============================================================================================================================
try {
    const raitings = document.querySelectorAll('.product__raiting');

    if (raitings.length > 0) {
        initRaitings();
    }


    function initRaitings() {
        let raitingActive;
        let raitingValue;

        for (let index = 0; index < raitings.length; index++) {
            const raiting = raitings[index];
            initRaiting(raiting);
        }

        function initRaiting(raiting) {
            initRaitingVars(raiting);
            setRaintingActiveWidth();
        };

        function initRaitingVars(raiting) {
            raitingActive = raiting.querySelector('.product__raiting-active');
            raitingValue = raiting.querySelector('.product__raiting-value');
        }

        function setRaintingActiveWidth(index = raitingValue.innerHTML) {
            const raitingActiveWidth = index / 0.05;
            raitingActive.style.width = `${raitingActiveWidth}%`;
        }
    };

} catch (error) { }


try {
    let favorites = document.querySelector('.favorites');
    let count = favorites.querySelector('.favorites__txt>.favorites__title-count>span');
    let favoritesItems = favorites.querySelectorAll('.products__item');
    count.innerHTML = favoritesItems.length;

} catch (error) { };

try {
    let truck = document.querySelector('.header__list-item._truck');
    setTruck(truck);

    function setTruck(item) {
        if (window.innerWidth > 960) {
            item.style.display = 'none';
        } else if (window.innerWidth < 400) {
            item.style.display = 'flex';
            item.innerHTML = '<i class="far fa-truck"></i>';
            item.style.marginRight = '5px';
            item.querySelector('i').style.marginRight = 0;
        } else {
            item.style.display = 'flex';
            item.innerHTML = '<i class="far fa-truck"></i> Доставка';

            item.style.marginRight = '25px';
        }
    }

    window.addEventListener('resize', (e) => setTruck(truck));
} catch (error) { }

try {
    let registrOrLogIn = document.querySelector('.registeration__links');
    let registerForms = document.querySelectorAll('.registeration__form');

    registrOrLogIn.addEventListener('click', (e) => {
        e.preventDefault();
        registerForms.forEach(item => item.classList.toggle('active'));
    });
} catch (error) { }

setTimeout(function(){
    document.getElementById('message').style.display = 'none';
}, 3000)