$(document).ready(function() {
  window.tab = "ideas";

  $('#tab-link-ideas').on("click", function(e) {
    e.preventDefault();
    if (window.tab == "ideas") {
      return;
    }
    window.tab = "ideas";
    $('.nav-link').removeClass("active");
    $('#tab-link-ideas').addClass("active");
    $('#tab-link-gift-search').removeClass("active");
    $('#tab-gift-search').hide(200);
    $('#tab-ideas').show(200);
  });
  
  $('#tab-link-gift-search').on("click", function(e) {
    e.preventDefault();
    if (window.tab == "gift-search") {
      return;
    }
    window.tab = "gift-search";
    $('.nav-link').removeClass("active");
    $('#tab-link-ideas').removeClass("active");
    $('#tab-link-gift-search').addClass("active");
    $('#tab-ideas').hide(200);
    $('#tab-gift-search').show(200);
  });
  
  $('#age').on("mousemove", function(e) {
    $('#age-label').text($('#age').val());
  });
  $('#age').on("change", function(e) {
    $('#age-label').text($('#age').val());
  });
  
  $('.card-hobby').on("click", function(e) {
    e.preventDefault();
    $(e.target).children(".card-hobby-checkbox").toggleClass("mdi-checkbox-blank-outline");
    $(e.target).children(".card-hobby-checkbox").toggleClass("mdi-checkbox-marked");
    if (this.getAttribute("checked") === "true") {
      this.setAttribute("checked", "false");
    } else {
      this.setAttribute("checked", "true");
    }
  });

  $('#findit').on("click", function(e) {
    $('#tab-ideas, #tab-gift-search').hide(200);
    $('#loading-overlay').toggleClass("active");
    window.scrollTo({ top: 0, behavior: "instant" });
    $('#tab-ideas, #tab-gift-search').removeClass("active");
    $('nav').hide();
    // $('body').css({
    //   overflow: 'hidden'
    // });

    fetch(window.urls.findGift, {
      method: "POST",
      body: JSON.stringify({
        age: $('#age').val(),
        gender: [
          $('#gender-f'),
          $('#gender-m'),
          $('#gender-o')
        ].filter(g => !!g.prop("checked"))[0].attr("id").substring(7).toUpperCase(),
        hobbies: [...document.querySelectorAll(".card-hobby[checked=true]")].map(card => parseInt(card.getAttribute("data-hobby-pk")))
      }),
      headers: {
        "X-CSRFToken": window.csrf_token,
        "Content-Type": "application/json"
      }
    }).then(res => res.json()).then(j => {
      const [top, ...others] = j;
      $('#card-top-product-name').text(top.name);
      $('#card-top-product-img').attr("src", top.image_url);
      $('#card-top-product-stars').html(`${(top.stars / 10).toFixed(1)} &#9733;`);
      $('#card-top-product-price').html(`$ ${(top.price / 100).toFixed(2)}`);
      if (top.is_bestseller) {
        $('#card-top-product-bestseller').removeClass("d-none");
      }
      $('#card-top-product-url').attr("href", top.product_url);

      others.forEach(element => {
        const row = $(
          `<div class="d-flex flex-row my-3 mx-1 align-items-center">
            <div style="min-width: 8rem;">
              <img src="${element.image_url}" class="img-fluid p-2" style="width: auto; height: auto; max-width: 6rem; max-height: 6rem; margin-top: -0rem;">
            </div>
            <div class="d-flex flex-column">
              <span class="p-0 m-1 mb-0 rubik-400 text-start" style="font-size: 1.1rem; overflow: hidden; display: -webkit-box; text-overflow: ellipsis; -webkit-line-clamp: 4; line-clamp: 4; -webkit-box-orient: vertical;">${element.name}</span>
              <div class="d-flex flex-row mx-1 align-items-center">
                <span class="p-0 m-0 rubik-500 text-start" style="font-size: 1.1rem;">$ ${(top.price / 100).toFixed(2)}</span>
                &nbsp;&bull;&nbsp;
                <span class="p-0 m-0 rubik-400 text-start" style="font-size: 1.1rem;">${(top.stars / 10).toFixed(1)} &#9733;</span>
                &nbsp;&bull;&nbsp;
                <span class="p-0 m-0 rubik-400 text-start" style="font-size: 1.1rem;"><a href="${element.product_url}">View</a></span>
              </div>
            </div>
          </div>`);
        $('#card-other-products-container').append(row);
      });

      setTimeout(() => {
        $('nav').hide();
        $('#loading-overlay').toggleClass("active");
        $('#tab-ideas, #tab-gift-search').hide();
        $('#tab-results').show();
      }, 1000);
    }).catch(err => { console.log(err)});
  });

  window.loadRandomProduct = function() {
    window.isSwiping = false;
    fetch(window.urls.randomProducts).then(res => res.json()).then(j => {
      $('#card-random-product-img').attr("src", j.image_url);
      $('#card-random-product-name').text(j.name);
      window.randomProduct = j;
    }).catch(err => {});
  }

  const swiped = function(draggable) {
    const offset = $(draggable).offset();
    const offsetParent = $(draggable).offsetParent().offset();
    const middlePointWindowRatio = (offset.left - offsetParent.left + $(draggable).width() / 2.0) / window.innerWidth;
    if (middlePointWindowRatio <= 0) {
      return "left";
    } else if (middlePointWindowRatio >= 1.0) {
      return "right";
    }
    return null;
  }

  window.isSwiping = false;
  $('#card-random-product').draggable({
    drag: function() {
      if (window.isSwiping) {
        return;
      }
      window.isSwiping = true;
      if (swiped(this) === "right") {
        $('#yes-overlay').addClass("active");
        setTimeout(() => {
          fetch(window.urls.restRandomFeedback, {
            method: "POST",
            body: JSON.stringify(window.j),
            headers: {
              "X-CSRFToken": window.csrf_token,
              "Content-Type": "application/json"
            }
          }).then(res => res.json()).then(j => {
            $('#yes-overlay').removeClass("active");
            window.loadRandomProduct();
          }).catch(err => {
            $('#yes-overlay').removeClass("active");
            window.loadRandomProduct();
          });
        }, 1000);
      } else if (swiped(this) === "left") {
        $('#no-overlay').addClass("active");
        setTimeout(() => {
          fetch(window.urls.restRandomFeedback, {
            method: "POST",
            body: JSON.stringify(window.j),
            headers: {
              "X-CSRFToken": window.csrf_token,
              "Content-Type": "application/json"
            }
          }).then(res => res.json()).then(j => {
            $('#no-overlay').removeClass("active");
            window.loadRandomProduct();
          }).catch(err => {
            $('#no-overlay').removeClass("active");
            window.loadRandomProduct();
          });
        }, 1000);
      } else {
        window.isSwiping = false;
      }
    },
    stop: function() {
      $(this).css({ top: 0, left: 0 });
    },
    axis: "x",
    revert: function() {
      return true;
    },
    scroll: false
  });
  $('#skip').on("click", function(e) {
    loadRandomProduct();
  });

  window.loadRandomProduct();
  $('#tab-ideas').show();
});