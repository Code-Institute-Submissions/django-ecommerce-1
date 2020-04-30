// initialise tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// make menu sticky once scroll past it
var menuBarId = '#menu-nav-bar';
// once the user goes beyond this point the menu becomes sticky
var stickyPoint = 124;

$(document).ready(() => {
    $(window).scroll(() => {
        if ($(window).scrollTop() > stickyPoint) {
            $(menuBarId).addClass('fixed-top');
        } else {
            $(menuBarId).removeClass('fixed-top');
        }
    });
});


// carousel ids
var bestsellerCarousel = '#carousel-most-popular';
var newProductCarousel = '#carousel-new-products';

// individual carousel item selector classes
var bestSellerIdentifier = '.most-popular';
var newProductIdentifier = '.new-products';

// generic item selector class - will be differentiated via parent-child relationship
var carouselInner = '.carousel-inner';

// list all carousels, seperated by ','
var carousels = bestsellerCarousel + ', ' + newProductCarousel;


// homepage carousel event listener
$(carousels).on('slide.bs.carousel', function (e) {
    /* CC 2.0 License Iatek LLC 2018 - Attribution required 
    ---------    
    Modified for the purpose of using multiple carousels on one page
    for CI django ecommerce project*/

    var $e = $(e.relatedTarget);

    var carousel;
    var item;

    if (this.id == bestsellerCarousel.substr(1)) {
        carousel = bestsellerCarousel;
        item = bestSellerIdentifier;
    } else {
        carousel = newProductCarousel;
        item = newProductIdentifier;
    }

    // given multiple carousels, select child inner of event carousel
    var carouselInnerIdentifier = carousel + ' > ' + carouselInner;

    var idx = $e.index();
    var itemsPerSlide = 4;

    var totalItems = $(item).length;

    if (idx >= totalItems - (itemsPerSlide - 1)) {
        var it = itemsPerSlide - (totalItems - idx);
        for (var i = 0; i < it; i++) {
            // append slides to end
            if (e.direction == 'left') {
                $(item).eq(i).appendTo(carouselInnerIdentifier);
            } else {
                $(item).eq(0).appendTo(carouselInnerIdentifier);
            }
        }
    }
});


/* product detail page tab class correction:
 bootstrap adds classes to the child element (a), I need it on the parent
 element (li)
*/

$('#product-tabs a').click(function (e) {
    // prevent bootstrap default aciton
    e.preventDefault();
    // select and remove the 'active' class from the li that current has it
    $('#product-tabs .active').removeClass('active');
    // add 'active' class to the target li tag (parent of the <a> tag)
    $(this).parent().addClass('active');
});